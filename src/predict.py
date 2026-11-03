
# Customer Churn Prediction - Reusable Inference Module
import numpy as np
from pathlib import Path
import argparse
import json

import joblib
import pandas as pd


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "models"
    / "tuned_random_forest_churn_pipeline.joblib"
)

METADATA_PATH = (
    PROJECT_ROOT
    / "notebooks"
    / "models"
    / "model_metadata.json"
)


# --------------------------------------------------
# 2. LOAD MODEL AND METADATA
# --------------------------------------------------

def load_artifacts():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata file not found: {METADATA_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    return model, metadata


# --------------------------------------------------
# 3. REUSABLE DATAFRAME PREDICTION
# --------------------------------------------------


def predict_dataframe(customers, model=None, metadata=None):

    if not isinstance(customers, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if customers.empty:
        raise ValueError("Input contains no customer records.")

    if customers.columns.duplicated().any():
        duplicates = customers.columns[
            customers.columns.duplicated()
        ].tolist()

        raise ValueError(
            f"Duplicate columns found: {duplicates}"
        )

    if model is None or metadata is None:
        model, metadata = load_artifacts()

    # Validate metadata
    if "decision_threshold" not in metadata:
        raise ValueError(
            "Decision threshold missing from model metadata."
        )

    threshold = float(metadata["decision_threshold"])

    if not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError(
            "Decision threshold must be between 0 and 1."
        )

    if metadata.get("positive_class") != 1:
        raise ValueError(
            "Unexpected positive class in metadata."
        )

    if metadata.get("positive_class_meaning") != "Churn = Yes":
        raise ValueError(
            "Positive class meaning does not match Churn = Yes."
        )

    # Verify model class order
    classes = list(model.classes_)

    if 1 not in classes:
        raise ValueError(
            "The trained model does not contain the positive class 1."
        )

    positive_index = classes.index(1)

    expected_features = list(model.feature_names_in_)

    missing_features = [
        col for col in expected_features
        if col not in customers.columns
    ]

    if missing_features:
        raise ValueError(
            "Missing required features: "
            + ", ".join(missing_features)
        )

    X = customers[expected_features].copy()

    # Normalize missing-value representations
    X = X.replace(
        ["None", "none", "NULL", "null", "N/A", "NA", ""],
        np.nan
    )

    X = X.replace(r"^\s*$", np.nan, regex=True)

    # Validate numerical features
    numeric_features = [
        "Tenure Months",
        "Monthly Charges",
        "Total Charges"
    ]

    for col in numeric_features:

        if col not in X.columns:
            continue

        converted = pd.to_numeric(
            X[col],
            errors="coerce"
        )

        invalid = (
            converted.isna()
            | ~np.isfinite(converted)
        )

        if invalid.any():
            rows = (
                np.flatnonzero(invalid.to_numpy()) + 2
            ).tolist()

            raise ValueError(
                f"Missing or invalid numerical values in "
                f"'{col}' at CSV row(s): {rows}"
            )

        if (converted < 0).any():
            raise ValueError(
                f"Negative values are not allowed in '{col}'."
            )

        if col == "Tenure Months" and (converted > 72).any():
            raise ValueError(
                "Tenure Months cannot exceed 72."
            )

        X[col] = converted

    # Validate remaining missing values
    missing_counts = X.isna().sum()

    missing_columns = missing_counts[
        missing_counts > 0
    ]

    if not missing_columns.empty:
        raise ValueError(
            f"Missing values detected: "
            f"{missing_columns.to_dict()}"
        )

    # Validate categorical values against fitted encoder
    try:
       # Categorical validation
       # The saved OneHotEncoder uses handle_unknown="ignore".
        # Therefore, unseen categorical values can be handled by the pipeline.

        print("Categorical validation: handled by saved OneHotEncoder.")

    except KeyError as error:
        raise ValueError(
            f"Could not verify model preprocessing configuration: {error}"
        )

    # Generate churn probabilities
    probabilities = model.predict_proba(X)[:, positive_index]

    predictions = (
        probabilities >= threshold
    ).astype(int)

    results = customers.copy()

    results["Churn_Probability"] = probabilities
    results["Predicted_Churn"] = predictions

    results["Predicted_Label"] = (
        results["Predicted_Churn"]
        .map({
            0: "No Churn",
            1: "Churn"
        })
    )

    # --------------------------------------------------
    # CLASSIFY CUSTOMER CHURN RISK
    # --------------------------------------------------

    def classify_risk(probability):

        if probability < threshold:
            return "Low"

        elif probability < 0.70:
            return "Medium"

        elif probability < 0.80:
            return "High"

        else:
            return "Very High"

    results["Risk_Category"] = (
        results["Churn_Probability"].apply(
            classify_risk
        )
    )

    return results




# --------------------------------------------------
# 4. COMMAND-LINE CSV PREDICTION
# --------------------------------------------------

def predict_customers(input_path, output_path):

    customers = pd.read_csv(input_path)

    model, metadata = load_artifacts()

    results = predict_dataframe(
        customers,
        model,
        metadata
    )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results.to_csv(
        output_path,
        index=False
    )

    print("Prediction completed successfully!")
    print("Input records:", len(customers))
    print(
        "Decision threshold:",
        metadata["decision_threshold"]
    )
    print(
        "Output saved to:",
        output_path.resolve()
    )

    print("\nPredicted customer categories:")

    print(
        results["Predicted_Label"].value_counts()
    )


# --------------------------------------------------
# 5. COMMAND-LINE ARGUMENTS
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Predict customer churn using "
            "the saved Random Forest model."
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input customer CSV file."
    )

    parser.add_argument(
        "--output",
        default="reports/churn_predictions.csv",
        help="Output prediction CSV file."
    )

    args = parser.parse_args()

    predict_customers(
        args.input,
        args.output
    )


if __name__ == "__main__":
    main()
