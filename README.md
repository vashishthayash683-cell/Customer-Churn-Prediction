# Customer Churn Prediction

## Project Overview

Customer Churn Prediction is a machine learning project developed to identify customers who are likely to discontinue a company's services.

The project uses customer demographic information, subscribed services, account details, and billing information to predict customer churn.

The objective is to help businesses identify potentially churning customers and support data-driven customer retention strategies.

## Objectives

- Analyze customer data and identify churn patterns.
- Perform exploratory data analysis (EDA).
- Prepare categorical and numerical features for machine learning.
- Train and compare multiple classification models.
- Optimize model hyperparameters.
- Evaluate model performance using multiple classification metrics.
- Generate reusable predictions for new customer records.

## Dataset

- Dataset: Telco Customer Churn
- Source file: `Telco_customer_churn.xlsx`
- Total records: 7,043
- Original columns: 33
- Target variable: `Churn Label`
- Positive class: Yes (Churn)

## Technologies and Tools

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook
- Joblib
- VS Code

## Project Workflow

1. Data loading and inspection
2. Data cleaning and preprocessing
3. Exploratory Data Analysis
4. Feature selection
5. Train-test splitting
6. Baseline model development
7. Model comparison
8. Stratified cross-validation
9. Hyperparameter tuning
10. Decision threshold optimization
11. Feature importance analysis
12. Model evaluation
13. Model serialization
14. Reusable prediction script development

## Machine Learning Models

The following classification models were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Dummy Classifier (baseline)

The Random Forest model was selected as the provisional final model after model comparison and hyperparameter tuning.

## Model Performance

Final tuned Random Forest test-set results at a decision threshold of 0.52:

| Metric | Score |
|---|---:|
| Accuracy | 76.58% |
| Precision | 54.18% |
| Recall | 76.20% |
| F1-score | 63.33% |
| ROC-AUC | 85.32% |
| PR-AUC | 66.96% |

The model uses a decision threshold of 0.52 to classify customers as likely to churn or not churn.

**Evaluation note:** The test set was also used during earlier model comparisons. Therefore, these results should be treated as an evaluation estimate rather than a completely untouched final test result.

## Model Explainability

The Random Forest feature importance analysis identified several influential features:

- Month-to-month contract
- Tenure Months
- Total Charges
- Two-year contract
- Monthly Charges

Feature importance indicates model associations and should not be interpreted as proof of causation.

## Project Structure

```text
Zidio_Customer_Churn/
│
├── data/
│   └── Telco_customer_churn.xlsx
│
├── notebooks/
│   ├── models/
│   │   ├── tuned_random_forest_churn_pipeline.joblib
│   │   └── model_metadata.json
│   │
│   ├── customer_churn_analysis.ipynb
│   └── sample_customers.csv
│
├── reports/
│   └── churn_predictions.csv
│
├── src/
│   └── predict.py
│
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Zidio_Customer_Churn
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Prediction Script

Provide a CSV file containing the required 19 model features.

Run:

```bash
python src/predict.py --input notebooks/sample_customers.csv
```

The script generates predictions and saves the output to:

```text
reports/churn_predictions.csv
```

The output includes:

- Churn Probability
- Predicted Churn (0 or 1)
- Predicted Label (Churn / No Churn)

## Future Improvements

- Develop an interactive customer churn dashboard.
- Explore additional classification algorithms.
- Perform further model calibration.
- Evaluate performance on a completely untouched external test dataset.
- Deploy the model through a web application or API.

## Author

Yash Vashishtha

Customer Churn Prediction — Machine Learning Project