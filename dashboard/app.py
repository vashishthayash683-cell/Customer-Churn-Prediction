
from pathlib import Path
import sys
import hashlib

import pandas as pd
import plotly.express as px
import streamlit as st

# Import reusable prediction module
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.predict import predict_dataframe, load_artifacts


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "Telco_customer_churn.xlsx"

SHEET_NAME = "Telco_Churn"

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 2. PROFESSIONAL DASHBOARD UI — GLOBAL THEME
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* ==============================
       GLOBAL APPLICATION
    ============================== */

    :root {
        --primary: #2563EB;
        --primary-dark: #1D4ED8;
        --navy: #14213D;
        --background: #F4F7FC;
        --surface: #FFFFFF;
        --text-primary: #172033;
        --text-secondary: #64748B;
        --border: #E5EAF2;
        --success: #16A34A;
        --danger: #DC2626;
    }

    .stApp {
        background: var(--background);
        color: var(--text-primary);
    }

    [data-testid="stHeader"] {
        background: rgba(244, 247, 252, 0.85);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ==============================
       TYPOGRAPHY
    ============================== */

    h1 {
        color: var(--navy) !important;
        font-size: 2rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.7px;
    }

    h2 {
        color: var(--navy) !important;
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }

    h3 {
        color: #253858 !important;
        font-size: 1.12rem !important;
        font-weight: 650 !important;
    }

    p, li {
        color: #475569;
        line-height: 1.65;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--text-secondary);
        font-size: 0.82rem;
    }

    .main-title {
        font-size: 2rem;
        font-weight: 800;
        color: var(--navy);
        letter-spacing: -0.8px;
        margin-bottom: 5px;
    }

    .subtitle {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 26px;
    }

    /* ==============================
       SIDEBAR
    ============================== */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #101D35 0%,
            #172B4D 100%
        );
        border-right: 1px solid #263B60;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption {
        color: #E8EEF9 !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        padding: 10px 12px;
        border-radius: 9px;
        transition: background 0.2s ease;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #263B60;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] p {
        color: #E8EEF9 !important;
        font-size: 0.92rem;
        font-weight: 500;
    }

    [data-testid="stSidebar"] hr {
        border-color: #344967;
    }

    /* ==============================
   KPI METRIC CARDS
============================== */

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #FFFFFF 0%,
        #F9FBFF 100%
    );
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 21px 22px;
    min-height: 120px;

    box-shadow:
        0 2px 8px rgba(15, 23, 42, 0.035),
        0 8px 20px rgba(15, 23, 42, 0.025);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: #BFDBFE;

    box-shadow:
        0 5px 14px rgba(15, 23, 42, 0.06),
        0 12px 25px rgba(37, 99, 235, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 0.84rem !important;
    font-weight: 650 !important;
    letter-spacing: 0.15px;
}

[data-testid="stMetricValue"] {
    color: #14213D !important;
    font-size: 1.85rem !important;
    font-weight: 750 !important;
    letter-spacing: -0.6px;
}

[data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}

@media (max-width: 768px) {
    [data-testid="stMetric"] {
        padding: 15px;
        min-height: 100px;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
}

/* ------------------------------------------
   KPI CARD ALIGNMENT & RESPONSIVENESS
------------------------------------------ */

[data-testid="stHorizontalBlock"] {
    align-items: stretch;
}

[data-testid="stMetric"] {
    min-height: 115px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow-wrap: anywhere;
}

[data-testid="stMetricLabel"] {
    min-height: 28px;
}

@media (max-width: 900px) {
    [data-testid="stMetric"] {
        min-height: 105px;
    }
}

@media (max-width: 600px) {
    [data-testid="stMetric"] {
        min-height: 95px;
        padding: 12px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 22px;
    }
}

    /* ==============================
       CHART CONTAINERS
    ============================== */

    [data-testid="stPlotlyChart"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 10px 10px 2px 10px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.025);
    }

    /* ==============================
       DATAFRAMES AND TABLES
    ============================== */

    [data-testid="stDataFrame"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    /* ==============================
       BUTTONS
    ============================== */

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 9px;
        font-weight: 650;
        min-height: 42px;
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {
        background: var(--primary);
        border: 1px solid var(--primary);
        color: white;
    }

    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover {
        background: var(--primary-dark);
        border-color: var(--primary-dark);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    /* ==============================
       INPUTS AND FILTERS
    ============================== */

    [data-testid="stSelectbox"],
    [data-testid="stMultiSelect"],
    [data-testid="stSlider"],
    [data-testid="stFileUploader"] {
        background: transparent;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        border-radius: 8px;
    }

    [data-testid="stFileUploader"] section {
        background: #FFFFFF;
        border: 1px dashed #A8B8D0;
        border-radius: 12px;
    }

    /* ==============================
       EXPANDERS
    ============================== */

    [data-testid="stExpander"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    /* ==============================
       ALERTS AND NOTIFICATIONS
    ============================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
        border: 1px solid var(--border);
    }

    /* ==============================
       DIVIDERS AND SPACING
    ============================== */

    hr {
        border-color: var(--border);
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    /* ==============================
       RESPONSIVE LAYOUT
    ============================== */

    @media (max-width: 768px) {

        .block-container {
            padding: 1rem 1rem 2rem 1rem;
        }

        .main-title {
            font-size: 1.65rem;
        }

        h1 {
            font-size: 1.65rem !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.35rem !important;
        }
    }
    /* ==========================================
   PAGE LAYOUT & VISUAL CONSISTENCY
========================================== */

/* Main dashboard content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Consistent page headings */
.main-title {
    font-size: 2rem;
    font-weight: 750;
    letter-spacing: -0.7px;
    margin-bottom: 0.35rem;
}

/* Page subtitles */
.subtitle {
    font-size: 0.95rem;
    color: #64748b;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

/* Section headings */
h2 {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    margin-top: 1.5rem !important;
    margin-bottom: 0.8rem !important;
}

/* Subsection headings */
h3 {
    font-size: 1.08rem !important;
    font-weight: 650 !important;
}

/* Consistent horizontal spacing */
div[data-testid="stHorizontalBlock"] {
    gap: 1rem;
}

/* Consistent divider appearance */
hr {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    border-color: #e2e8f0;
}

/* Responsive layout */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 2rem 1rem;
    }

    h1 {
        font-size: 1.65rem !important;
    }

    h2 {
        font-size: 1.2rem !important;
    }
}
    /* Sidebar navigation polish */
section[data-testid="stSidebar"] {
    border-right: 1px solid #e2e8f0;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    letter-spacing: -0.3px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 0.4rem;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius: 8px;
    padding: 0.45rem 0.65rem;
    transition: background 0.2s ease;
}
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 3. LOAD DATASET
# --------------------------------------------------

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    data = pd.read_excel(
        DATA_PATH,
        sheet_name=SHEET_NAME
    )

    data["Churn Label"] = (
        data["Churn Label"]
        .astype(str)
        .str.strip()
    )

    return data


try:
    df = load_data()

except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()


# --------------------------------------------------
# 4. SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("📊 Churn Analytics")

    st.caption("Customer Intelligence Platform")

    st.divider()

    selected_page = st.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "Customer Analytics",
        "Model Performance",
        "Churn Prediction"
    ],
    index=0,
    label_visibility="visible"
)
    st.divider()

    st.caption("PROJECT INFORMATION")
    st.write("Dataset: Telco Customer Churn")
    st.write(f"Records: {len(df):,}")
    st.write("Model: Tuned Random Forest")

   

# --------------------------------------------------
# 5. EXECUTIVE OVERVIEW — BUSINESS INTELLIGENCE
# --------------------------------------------------

if selected_page == "Executive Overview":

    # --------------------------------------------------
    # A. HEADER
    # --------------------------------------------------

    st.markdown(
        '<div class="main-title">Executive Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A high-level view of customer churn, retention performance, and business impact.</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # B. DATA PREPARATION
    # --------------------------------------------------

    overview_df = df.copy()

    overview_df["Churn Label"] = (
        overview_df["Churn Label"].astype(str).str.strip()
    )

    total_customers = len(overview_df)

    churned_customers = (
        overview_df["Churn Label"] == "Yes"
    ).sum()

    retained_customers = (
        overview_df["Churn Label"] == "No"
    ).sum()

    churn_rate = (
        churned_customers / total_customers * 100
        if total_customers else 0
    )

    retention_rate = (
        retained_customers / total_customers * 100
        if total_customers else 0
    )

    churned_df = overview_df[
        overview_df["Churn Label"] == "Yes"
    ]

    retained_df = overview_df[
        overview_df["Churn Label"] == "No"
    ]

    avg_monthly_charges = overview_df[
        "Monthly Charges"
    ].mean()

    churned_avg_monthly_charges = churned_df[
        "Monthly Charges"
    ].mean()

        # --------------------------------------------------
    # C. EXECUTIVE KPI CARDS
    # --------------------------------------------------

    st.subheader("Business Performance Indicators")

    st.caption(
        "Key metrics summarising customer base, churn performance, "
        "and customer retention."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Total Customers",
        value=f"{total_customers:,}",
        help="Total number of customers included in the analysis."
    )

    col2.metric(
        label="Churned Customers",
        value=f"{churned_customers:,}",
        help="Number of customers who discontinued the service."
    )

    col3.metric(
        label="Retained Customers",
        value=f"{retained_customers:,}",
        help="Number of customers who continue using the service."
    )

    col4.metric(
        label="Customer Churn Rate",
        value=f"{churn_rate:.2f}%",
        help="Percentage of customers who discontinued the service."
    )

    st.divider()

    
    # --------------------------------------------------
    # D. CUSTOMER RETENTION SNAPSHOT
    # --------------------------------------------------

    st.subheader("Customer Retention Snapshot")

    st.caption(
        "Distribution of retained and churned customers "
        "across the analysed customer base."
    )

    left_col, right_col = st.columns([1.3, 1])

    with left_col:

        retention_data = pd.DataFrame({
            "Customer Status": [
                "Churned",
                "Retained"
            ],
            "Customers": [
                churned_customers,
                retained_customers
            ]
        })

        fig_retention = px.pie(
            retention_data,
            names="Customer Status",
            values="Customers",
            hole=0.68,
            color="Customer Status",
            color_discrete_map={
                "Churned": "#EF4444",
                "Retained": "#2563EB"
            }
        )

        fig_retention.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont=dict(
                size=13,
                color="white"
            ),
            marker=dict(
                line=dict(
                    color="white",
                    width=3
                )
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Customers: %{value:,}<br>"
                "Customer Share: %{percent:.1%}"
                "<extra></extra>"
            )
        )

        fig_retention.update_layout(
            title=dict(
                text="Customer Churn Distribution",
                x=0.5,
                xanchor="center",
                font=dict(size=17)
            ),
            annotations=[
                dict(
                    text=f"<b>{total_customers:,}</b><br>"
                         "<span style='font-size:11px'>Total Customers</span>",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=19)
                )
            ],
            margin=dict(t=65, b=25, l=20, r=20),
            legend_title_text="Customer Status",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.12,
                xanchor="center",
                x=0.5
            ),
            height=390
        )

        st.plotly_chart(
            fig_retention,
            width="stretch",
            config={"displayModeBar": False}
        )

    with right_col:

        st.markdown("#### Retention Summary")

        st.caption(
            "Key billing and customer retention indicators."
        )

        st.metric(
            label="Customer Retention Rate",
            value=f"{retention_rate:.2f}%",
            help="Percentage of customers who continue using the service."
        )

        st.metric(
            label="Average Monthly Charges",
            value=f"${avg_monthly_charges:,.2f}",
            help="Average monthly billing amount across the analysed customer base."
        )

        st.metric(
            label="Churned Customers' Average Monthly Charges",
            value=f"${churned_avg_monthly_charges:,.2f}",
            help="Average monthly charges among customers predicted or identified as churned in this dataset."
        )

        st.caption(
            "Monthly charges are descriptive billing figures "
            "and should not be interpreted as actual lost revenue."
        )

    st.divider()


    
    # --------------------------------------------------
    # E. CHURN RATE BY CONTRACT
    # --------------------------------------------------

    st.subheader("Contract-Based Churn Analysis")

    st.caption(
        "Compare customer churn rates across different "
        "contract categories to identify retention challenges."
    )

    contract_analysis = (
        overview_df.groupby("Contract")
        .agg(
            Total_Customers=("Churn Label", "count"),
            Churned_Customers=(
                "Churn Label",
                lambda values: (values == "Yes").sum()
            )
        )
        .reset_index()
    )

    contract_analysis["Churn Rate"] = (
        contract_analysis["Churned_Customers"]
        / contract_analysis["Total_Customers"].replace(0, pd.NA)
        * 100
    )

    contract_analysis = contract_analysis.dropna(
        subset=["Churn Rate"]
    ).sort_values(
        "Churn Rate",
        ascending=False
    )

    fig_contract = px.bar(
        contract_analysis,
        x="Contract",
        y="Churn Rate",
        color="Churn Rate",
        text="Churn Rate",
        color_continuous_scale="Reds",
        labels={
            "Contract": "Contract Type",
            "Churn Rate": "Churn Rate (%)"
        },
        hover_data={
            "Total_Customers": True,
            "Churned_Customers": True,
            "Churn Rate": ":.2f"
        }
    )

    fig_contract.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Churn Rate: %{y:.2f}%<br>"
            "Total Customers: %{customdata[0]:,}<br>"
            "Churned Customers: %{customdata[1]:,}"
            "<extra></extra>"
        )
    )

    fig_contract.update_layout(
        title=dict(
            text="Churn Rate Across Contract Types",
            x=0.5,
            xanchor="center"
        ),
        yaxis_title="Churn Rate (%)",
        xaxis_title="Contract Type",
        yaxis=dict(
            rangemode="tozero",
            ticksuffix="%",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.15)"
        ),
        coloraxis_showscale=False,
        margin=dict(t=70, b=45, l=35, r=35),
        height=420,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        )
    )

    st.plotly_chart(
        fig_contract,
        width="stretch",
        config={"displayModeBar": False}
    )

    st.divider()

    # --------------------------------------------------
    # F. TENURE-BASED CHURN ANALYSIS
    # --------------------------------------------------

    st.subheader("Customer Tenure and Churn Behaviour")

    st.caption(
        "Analyse how customer tenure relates to historical "
        "churn patterns across different customer segments."
    )

    tenure_df = overview_df.copy()

    tenure_df["Tenure Group"] = pd.cut(
        tenure_df["Tenure Months"],
        bins=[-1, 6, 12, 24, 48, 72],
        labels=[
            "0–6 Months",
            "7–12 Months",
            "13–24 Months",
            "25–48 Months",
            "49–72 Months"
        ]
    )

    tenure_analysis = (
        tenure_df.groupby(
            "Tenure Group",
            observed=False
        )
        .agg(
            Total_Customers=("Churn Label", "count"),
            Churned_Customers=(
                "Churn Label",
                lambda values: (values == "Yes").sum()
            )
        )
        .reset_index()
    )

    tenure_analysis["Churn Rate"] = (
        tenure_analysis["Churned_Customers"]
        / tenure_analysis["Total_Customers"].replace(0, pd.NA)
        * 100
    )

    tenure_analysis = tenure_analysis.dropna(
        subset=["Churn Rate"]
    )

    fig_tenure = px.bar(
        tenure_analysis,
        x="Tenure Group",
        y="Churn Rate",
        text="Churn Rate",
        color="Churn Rate",
        color_continuous_scale="OrRd",
        labels={
            "Tenure Group": "Customer Tenure",
            "Churn Rate": "Churn Rate (%)"
        },
        hover_data={
            "Total_Customers": True,
            "Churned_Customers": True,
            "Churn Rate": ":.2f"
        }
    )

    fig_tenure.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Churn Rate: %{y:.2f}%<br>"
            "Total Customers: %{customdata[0]:,}<br>"
            "Churned Customers: %{customdata[1]:,}"
            "<extra></extra>"
        )
    )

    fig_tenure.update_layout(
        title=dict(
            text="Churn Rate by Customer Tenure",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Customer Tenure",
        yaxis_title="Churn Rate (%)",
        yaxis=dict(
            rangemode="tozero",
            ticksuffix="%",
            showgrid=True,
            gridcolor="rgba(128,128,128,0.15)"
        ),
        coloraxis_showscale=False,
        margin=dict(t=70, b=45, l=35, r=35),
        height=420,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        )
    )

    st.plotly_chart(
        fig_tenure,
        width="stretch",
        config={"displayModeBar": False}
    )

    st.divider()

    # --------------------------------------------------
    # G. MONTHLY CHARGES ANALYSIS
    # --------------------------------------------------

    st.subheader("Monthly Charges and Churn Relationship")

    st.caption(
        "Compare monthly billing distributions between "
        "customers who churned and customers who were retained."
    )

    fig_charges = px.box(
        overview_df,
        x="Churn Label",
        y="Monthly Charges",
        color="Churn Label",
        color_discrete_map={
            "Yes": "#EF4444",
            "No": "#2563EB"
        },
        labels={
            "Churn Label": "Customer Status",
            "Monthly Charges": "Monthly Charges ($)"
        },
        points="outliers"
    )

    fig_charges.update_traces(
        marker=dict(size=5),
        line=dict(width=2),
        hovertemplate=(
            "<b>Customer Status: %{x}</b><br>"
            "Monthly Charges: $%{y:.2f}"
            "<extra></extra>"
        )
    )

    fig_charges.update_layout(
        title=dict(
            text="Monthly Charges Distribution by Customer Status",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Customer Status",
        yaxis_title="Monthly Charges ($)",
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(128,128,128,0.15)"
        ),
        showlegend=False,
        margin=dict(t=70, b=45, l=35, r=35),
        height=420,
        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        )
    )

    st.plotly_chart(
        fig_charges,
        width="stretch",
        config={"displayModeBar": False}
    )

    st.divider()

    # --------------------------------------------------
    # H. AUTOMATED BUSINESS INSIGHTS
    # --------------------------------------------------

    st.subheader("Key Business Insights")

    insight_col1, insight_col2 = st.columns(2)

    highest_contract = None

    if not contract_analysis.empty:
        highest_contract = contract_analysis.loc[
            contract_analysis["Churn Rate"].idxmax()
        ]

    highest_tenure_group = None

    if not tenure_analysis.empty:
        highest_tenure_group = tenure_analysis.loc[
            tenure_analysis["Churn Rate"].idxmax()
        ]

    with insight_col1:

        if highest_contract is not None:

            st.info(
                f"**Contract Insight**\n\n"
                f"{highest_contract['Contract']} customers have "
                f"the highest observed churn rate "
                f"({highest_contract['Churn Rate']:.2f}%) "
                f"among the contract categories."
            )

        else:
            st.info("Contract insights are unavailable for this dataset.")

        st.info(
            f"**Customer Retention Insight**\n\n"
            f"{retention_rate:.2f}% of customers in the "
            f"historical dataset are retained."
        )

    with insight_col2:

        if highest_tenure_group is not None:

            st.warning(
                f"**Tenure Insight**\n\n"
                f"The {highest_tenure_group['Tenure Group']} "
                f"tenure segment has the highest observed "
                f"churn rate "
                f"({highest_tenure_group['Churn Rate']:.2f}%)."
            )

        else:
            st.info("Tenure insights are unavailable for this dataset.")

        st.info(
            f"**Billing Insight**\n\n"
            f"Churned customers have average monthly charges "
            f"of ${churned_avg_monthly_charges:,.2f}."
        )

    # --------------------------------------------------
    # I. DATA SOURCE AND DISCLAIMER
    # --------------------------------------------------

    st.divider()

    st.caption(
        "Source: Telco Customer Churn dataset | "
        "All figures represent historical customer records. "
        "Observed relationships are descriptive and do not "
        "establish causation."
    )


# --------------------------------------------------
# 6. OTHER PAGES - COMING NEXT
# --------------------------------------------------



elif selected_page == "Customer Analytics":

    # --------------------------------------------------
    # A. PAGE HEADER
    # --------------------------------------------------

    st.markdown(
        '<div class="main-title">Customer Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Explore customer demographics, service usage, contract patterns, and churn behaviour.</div>',
        unsafe_allow_html=True
    )

    analytics_df = df.copy()

    # --------------------------------------------------
    # B. FILTER PANEL
    # --------------------------------------------------

    st.subheader("Customer Segmentation Filters")
    st.caption(
        "Select one or more values to dynamically analyse "
        "the matching customer population."
    )

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        selected_contracts = st.multiselect(
            "Contract Type",
            options=sorted(
                analytics_df["Contract"].dropna().unique().tolist()
            ),
            default=sorted(
                analytics_df["Contract"].dropna().unique().tolist()
            ),
            key="analytics_contract_filter"
        )

    with filter_col2:
        selected_internet = st.multiselect(
            "Internet Service",
            options=sorted(
                analytics_df["Internet Service"].dropna().unique().tolist()
            ),
            default=sorted(
                analytics_df["Internet Service"].dropna().unique().tolist()
            ),
            key="analytics_internet_filter"
        )

    with filter_col3:
        selected_payment = st.multiselect(
            "Payment Method",
            options=sorted(
                analytics_df["Payment Method"].dropna().unique().tolist()
            ),
            default=sorted(
                analytics_df["Payment Method"].dropna().unique().tolist()
            ),
            key="analytics_payment_filter"
        )

    filter_col4, filter_col5, filter_col6 = st.columns(3)

    with filter_col4:
        selected_gender = st.multiselect(
            "Gender",
            options=sorted(
                analytics_df["Gender"].dropna().unique().tolist()
            ),
            default=sorted(
                analytics_df["Gender"].dropna().unique().tolist()
            ),
            key="analytics_gender_filter"
        )

    with filter_col5:
        selected_senior = st.multiselect(
            "Senior Citizen",
            options=sorted(
                analytics_df["Senior Citizen"].dropna().unique().tolist()
            ),
            default=sorted(
                analytics_df["Senior Citizen"].dropna().unique().tolist()
            ),
            key="analytics_senior_filter"
        )

    with filter_col6:
        min_tenure = int(analytics_df["Tenure Months"].min())
        max_tenure = int(analytics_df["Tenure Months"].max())

        tenure_range = st.slider(
            "Tenure Range (Months)",
            min_value=min_tenure,
            max_value=max_tenure,
            value=(min_tenure, max_tenure),
            key="analytics_tenure_filter"
        )

    # --------------------------------------------------
    # C. APPLY FILTERS
    # --------------------------------------------------

    filtered_df = analytics_df[
        analytics_df["Contract"].isin(selected_contracts)
        & analytics_df["Internet Service"].isin(selected_internet)
        & analytics_df["Payment Method"].isin(selected_payment)
        & analytics_df["Gender"].isin(selected_gender)
        & analytics_df["Senior Citizen"].isin(selected_senior)
        & analytics_df["Tenure Months"].between(
            tenure_range[0],
            tenure_range[1]
        )
    ].copy()

    st.divider()

    if filtered_df.empty:

        st.warning(
            "No customers match the selected filters. "
            "Please adjust your filter selections."
        )

    else:

        # --------------------------------------------------
        # D. DYNAMIC CUSTOMER KPIs
        # --------------------------------------------------

        total_customers = len(filtered_df)

        churned_customers = (
            filtered_df["Churn Label"] == "Yes"
        ).sum()

        retained_customers = (
            filtered_df["Churn Label"] == "No"
        ).sum()

        churn_rate = (
            churned_customers / total_customers * 100
        )

        retention_rate = (
            retained_customers / total_customers * 100
        )

        avg_monthly_charges = (
            filtered_df["Monthly Charges"].mean()
        )

        st.subheader("Filtered Customer Overview")

        st.caption(
            "Key performance indicators based on the currently selected customer filters."
        )

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        kpi1.metric(
            label="Customers Analysed",
            value=f"{total_customers:,}",
            help="Total number of customers remaining after applying the selected filters."
        )

        kpi2.metric(
            label="Churned Customers",
            value=f"{churned_customers:,}",
            help="Number of filtered customers who discontinued the service."
        )

        kpi3.metric(
            label="Retained Customers",
            value=f"{retained_customers:,}",
            help="Number of filtered customers who continue using the service."
        )

        kpi4.metric(
            label="Customer Churn Rate",
            value=f"{churn_rate:.2f}%",
            help="Percentage of filtered customers who discontinued the service."
        )

        st.caption(
            f"Customer Retention Rate: {retention_rate:.2f}% | "
            f"Average Monthly Charges: ${avg_monthly_charges:,.2f}"
        )

        st.divider()

        # --------------------------------------------------
        # E. REUSABLE SEGMENT SUMMARY
        # --------------------------------------------------

        def create_segment_summary(data, column):

            summary = (
                data.groupby(column)
                .agg(
                    Total_Customers=("Churn Label", "count"),
                    Churned_Customers=(
                        "Churn Label",
                        lambda values: (values == "Yes").sum()
                    )
                )
                .reset_index()
            )

            summary["Churn Rate"] = (
                summary["Churned_Customers"]
                / summary["Total_Customers"].replace(0, pd.NA)
                * 100
            )

            return summary

        
        # --------------------------------------------------
        # F. CONTRACT AND INTERNET SERVICE ANALYSIS
        # --------------------------------------------------

        st.subheader("Service and Contract Analysis")

        st.caption(
            "Compare churn behaviour across contract types "
            "and internet service categories."
        )

        left_col, right_col = st.columns(2)

        with left_col:

            contract_summary = create_segment_summary(
                filtered_df,
                "Contract"
            ).dropna(
                subset=["Churn Rate"]
            ).sort_values(
                "Churn Rate",
                ascending=False
            )

            fig_contract = px.bar(
                contract_summary,
                x="Contract",
                y="Churn Rate",
                text="Churn Rate",
                color="Churn Rate",
                color_continuous_scale="Reds",
                labels={
                    "Contract": "Contract Type",
                    "Churn Rate": "Churn Rate (%)"
                },
                hover_data={
                    "Total_Customers": True,
                    "Churned_Customers": True,
                    "Churn Rate": ":.2f"
                }
            )

            fig_contract.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Churn Rate: %{y:.2f}%<br>"
                    "Total Customers: %{customdata[0]:,}<br>"
                    "Churned Customers: %{customdata[1]:,}"
                    "<extra></extra>"
                )
            )

            fig_contract.update_layout(
                title=dict(
                    text="Churn Rate by Contract",
                    x=0.5,
                    xanchor="center"
                ),
                xaxis_title="Contract Type",
                yaxis_title="Churn Rate (%)",
                yaxis=dict(
                    rangemode="tozero",
                    ticksuffix="%",
                    showgrid=True,
                    gridcolor="rgba(128,128,128,0.15)"
                ),
                showlegend=False,
                coloraxis_showscale=False,
                height=400,
                margin=dict(t=70, b=45, l=25, r=25)
            )

            st.plotly_chart(
                fig_contract,
                width="stretch",
                config={"displayModeBar": False}
            )

        with right_col:

            internet_summary = create_segment_summary(
                filtered_df,
                "Internet Service"
            ).dropna(
                subset=["Churn Rate"]
            ).sort_values(
                "Churn Rate",
                ascending=False
            )

            fig_internet = px.bar(
                internet_summary,
                x="Internet Service",
                y="Churn Rate",
                text="Churn Rate",
                color="Churn Rate",
                color_continuous_scale="Blues",
                labels={
                    "Internet Service": "Internet Service",
                    "Churn Rate": "Churn Rate (%)"
                },
                hover_data={
                    "Total_Customers": True,
                    "Churned_Customers": True,
                    "Churn Rate": ":.2f"
                }
            )

            fig_internet.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Churn Rate: %{y:.2f}%<br>"
                    "Total Customers: %{customdata[0]:,}<br>"
                    "Churned Customers: %{customdata[1]:,}"
                    "<extra></extra>"
                )
            )

            fig_internet.update_layout(
                title=dict(
                    text="Churn Rate by Internet Service",
                    x=0.5,
                    xanchor="center"
                ),
                xaxis_title="Internet Service",
                yaxis_title="Churn Rate (%)",
                yaxis=dict(
                    rangemode="tozero",
                    ticksuffix="%",
                    showgrid=True,
                    gridcolor="rgba(128,128,128,0.15)"
                ),
                showlegend=False,
                coloraxis_showscale=False,
                height=400,
                margin=dict(t=70, b=45, l=25, r=25)
            )

            st.plotly_chart(
                fig_internet,
                width="stretch",
                config={"displayModeBar": False}
            )

        st.divider()

        # --------------------------------------------------
        # G. PAYMENT METHOD AND GENDER ANALYSIS
        # --------------------------------------------------

        st.subheader("Customer Behaviour Analysis")

        st.caption(
            "Explore differences in churn behaviour across "
            "payment methods and customer demographics."
        )

        left_col, right_col = st.columns(2)

        with left_col:

            payment_summary = create_segment_summary(
                filtered_df,
                "Payment Method"
            ).dropna(
                subset=["Churn Rate"]
            ).sort_values(
                "Churn Rate",
                ascending=True
            )

            fig_payment = px.bar(
                payment_summary,
                x="Churn Rate",
                y="Payment Method",
                orientation="h",
                text="Churn Rate",
                color="Churn Rate",
                color_continuous_scale="OrRd",
                labels={
                    "Payment Method": "Payment Method",
                    "Churn Rate": "Churn Rate (%)"
                },
                hover_data={
                    "Total_Customers": True,
                    "Churned_Customers": True,
                    "Churn Rate": ":.2f"
                }
            )

            fig_payment.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Churn Rate: %{x:.2f}%<br>"
                    "Total Customers: %{customdata[0]:,}<br>"
                    "Churned Customers: %{customdata[1]:,}"
                    "<extra></extra>"
                )
            )

            fig_payment.update_layout(
                title=dict(
                    text="Churn Rate by Payment Method",
                    x=0.5,
                    xanchor="center"
                ),
                xaxis_title="Churn Rate (%)",
                yaxis_title="Payment Method",
                xaxis=dict(
                    rangemode="tozero",
                    ticksuffix="%",
                    showgrid=True,
                    gridcolor="rgba(128,128,128,0.15)"
                ),
                showlegend=False,
                coloraxis_showscale=False,
                height=430,
                margin=dict(t=70, b=45, l=25, r=50)
            )

            st.plotly_chart(
                fig_payment,
                width="stretch",
                config={"displayModeBar": False}
            )

        with right_col:

            gender_summary = create_segment_summary(
                filtered_df,
                "Gender"
            ).dropna(
                subset=["Churn Rate"]
            )

            fig_gender = px.bar(
                gender_summary,
                x="Gender",
                y="Churn Rate",
                text="Churn Rate",
                color="Gender",
                color_discrete_map={
                    "Male": "#2563EB",
                    "Female": "#EF4444"
                },
                labels={
                    "Gender": "Gender",
                    "Churn Rate": "Churn Rate (%)"
                },
                hover_data={
                    "Total_Customers": True,
                    "Churned_Customers": True,
                    "Churn Rate": ":.2f"
                }
            )

            fig_gender.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Churn Rate: %{y:.2f}%<br>"
                    "Total Customers: %{customdata[0]:,}<br>"
                    "Churned Customers: %{customdata[1]:,}"
                    "<extra></extra>"
                )
            )

            fig_gender.update_layout(
                title=dict(
                    text="Churn Rate by Gender",
                    x=0.5,
                    xanchor="center"
                ),
                xaxis_title="Gender",
                yaxis_title="Churn Rate (%)",
                yaxis=dict(
                    rangemode="tozero",
                    ticksuffix="%",
                    showgrid=True,
                    gridcolor="rgba(128,128,128,0.15)"
                ),
                showlegend=False,
                height=430,
                margin=dict(t=70, b=45, l=25, r=25)
            )

            st.plotly_chart(
                fig_gender,
                width="stretch",
                config={"displayModeBar": False}
            )

        st.divider()

        # --------------------------------------------------
        # H. TENURE SEGMENT ANALYSIS
        # --------------------------------------------------

        st.subheader("Customer Tenure Analysis")

        st.caption(
            "Understand how customer retention patterns vary "
            "across different tenure groups."
        )

        tenure_analysis = filtered_df.copy()

        tenure_analysis["Tenure Group"] = pd.cut(
            tenure_analysis["Tenure Months"],
            bins=[-1, 6, 12, 24, 48, 72],
            labels=[
                "0–6 Months",
                "7–12 Months",
                "13–24 Months",
                "25–48 Months",
                "49–72 Months"
            ]
        )

        tenure_summary = create_segment_summary(
            tenure_analysis,
            "Tenure Group"
        ).dropna(
            subset=["Churn Rate"]
        )

        fig_tenure = px.bar(
            tenure_summary,
            x="Tenure Group",
            y="Churn Rate",
            text="Churn Rate",
            color="Churn Rate",
            color_continuous_scale="OrRd",
            labels={
                "Tenure Group": "Customer Tenure",
                "Churn Rate": "Churn Rate (%)"
            },
            hover_data={
                "Total_Customers": True,
                "Churned_Customers": True,
                "Churn Rate": ":.2f"
            }
        )

        fig_tenure.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Churn Rate: %{y:.2f}%<br>"
                "Total Customers: %{customdata[0]:,}<br>"
                "Churned Customers: %{customdata[1]:,}"
                "<extra></extra>"
            )
        )

        fig_tenure.update_layout(
            title=dict(
                text="Churn Rate Across Customer Tenure Groups",
                x=0.5,
                xanchor="center"
            ),
            xaxis_title="Customer Tenure",
            yaxis_title="Churn Rate (%)",
            yaxis=dict(
                rangemode="tozero",
                ticksuffix="%",
                showgrid=True,
                gridcolor="rgba(128,128,128,0.15)"
            ),
            showlegend=False,
            coloraxis_showscale=False,
            height=420,
            margin=dict(t=70, b=45, l=25, r=25)
        )

        st.plotly_chart(
            fig_tenure,
            width="stretch",
            config={"displayModeBar": False}
        )

        st.divider()

        # --------------------------------------------------
        # I. MONTHLY CHARGES ANALYSIS
        # --------------------------------------------------

        st.subheader("Monthly Billing Analysis")

        st.caption(
            "Compare the distribution of monthly charges "
            "between churned and retained customers."
        )

        fig_charges = px.box(
            filtered_df,
            x="Churn Label",
            y="Monthly Charges",
            color="Churn Label",
            color_discrete_map={
                "Yes": "#EF4444",
                "No": "#2563EB"
            },
            points="outliers",
            labels={
                "Churn Label": "Customer Status",
                "Monthly Charges": "Monthly Charges ($)"
            },
            category_orders={
                "Churn Label": ["No", "Yes"]
            }
        )

        fig_charges.update_traces(
            marker=dict(size=5),
            line=dict(width=2),
            hovertemplate=(
                "<b>Customer Status: %{x}</b><br>"
                "Monthly Charges: $%{y:.2f}"
                "<extra></extra>"
            )
        )

        fig_charges.update_layout(
            title=dict(
                text="Monthly Charges by Customer Status",
                x=0.5,
                xanchor="center"
            ),
            xaxis_title="Customer Status",
            yaxis_title="Monthly Charges ($)",
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(128,128,128,0.15)"
            ),
            showlegend=False,
            height=420,
            margin=dict(t=70, b=45, l=25, r=25)
        )

        st.plotly_chart(
            fig_charges,
            width="stretch",
            config={"displayModeBar": False}
        )

        st.divider()


        
        # --------------------------------------------------
        # J. FILTERED CUSTOMER DATA
        # --------------------------------------------------

        st.subheader("Filtered Customer Records")

        st.caption(
            "Explore and download customer records matching "
            "the currently selected segmentation filters."
        )

        display_columns = [
            "Gender",
            "Senior Citizen",
            "Contract",
            "Internet Service",
            "Payment Method",
            "Tenure Months",
            "Monthly Charges",
            "Churn Label"
        ]

        display_df = filtered_df[display_columns].copy()

        display_df = display_df.rename(
            columns={
                "Senior Citizen": "Senior Citizen",
                "Tenure Months": "Tenure (Months)",
                "Monthly Charges": "Monthly Charges ($)",
                "Churn Label": "Customer Status"
            }
        )

        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True,
            column_config={
                "Gender": st.column_config.TextColumn(
                    "Gender"
                ),
                "Senior Citizen": st.column_config.TextColumn(
                    "Senior Citizen"
                ),
                "Contract": st.column_config.TextColumn(
                    "Contract"
                ),
                "Internet Service": st.column_config.TextColumn(
                    "Internet Service"
                ),
                "Payment Method": st.column_config.TextColumn(
                    "Payment Method"
                ),
                "Tenure (Months)": st.column_config.NumberColumn(
                    "Tenure (Months)",
                    format="%d"
                ),
                "Monthly Charges ($)": st.column_config.NumberColumn(
                    "Monthly Charges ($)",
                    format="$%.2f"
                ),
                "Customer Status": st.column_config.TextColumn(
                    "Customer Status"
                )
            }
        )

        st.caption(
            f"Displaying {len(display_df):,} customer records."
        )

        # CSV DOWNLOAD

        filtered_csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Filtered Customer Data (CSV)",
            data=filtered_csv,
            file_name="filtered_customer_analytics.csv",
            mime="text/csv",
            width="stretch",
            key="download_filtered_customer_analytics"
        )

        # --------------------------------------------------
        # K. SOURCE NOTE
        # --------------------------------------------------

        st.divider()

        st.caption(
            "Source: Telco Customer Churn dataset. "
            "All metrics and charts are dynamically calculated "
            "from the selected customer segment. "
            "Observed associations do not establish causation."
        )






elif selected_page == "Model Performance":

    st.title("Model Performance")
    st.caption(
        "A detailed evaluation of churn prediction models, "
        "cross-validation results and classification performance."
    )

    # --------------------------------------------------
    # 1. MODEL PERFORMANCE DATA
    # --------------------------------------------------

    comparison_data = pd.DataFrame({
        "Model": [
            "Logistic Regression",
            "Random Forest",
            "Decision Tree",
            "Dummy Classifier"
        ],
        "Accuracy": [0.8020, 0.7892, 0.7395, 0.7346],
        "Precision": [0.6435, 0.5937, 0.5061, 0.0000],
        "Recall": [0.5695, 0.6524, 0.7781, 0.0000],
        "F1 Score": [0.6043, 0.6217, 0.6133, 0.0000],
        "ROC-AUC": [0.8489, 0.8461, 0.8248, 0.5000],
        "PR-AUC": [0.6453, 0.6481, 0.6207, 0.2654]
    })

    cv_data = pd.DataFrame({
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC-AUC",
            "PR-AUC"
        ],
        "Tuned Random Forest": [
            0.7735, 0.5518, 0.7886,
            0.6490, 0.8613, 0.6757
        ],
        "Tuned Logistic Regression": [
            0.7609, 0.5330, 0.8074,
            0.6419, 0.8584, 0.6788
        ]
    })

    test_data = pd.DataFrame({
        "Model": [
            "Tuned Logistic Regression",
            "Tuned Random Forest"
        ],
        "Accuracy": [0.7630, 0.7658],
        "Precision": [0.5392, 0.5418],
        "Recall": [0.7353, 0.7620],
        "F1 Score": [0.6222, 0.6333],
        "ROC-AUC": [0.8485, 0.8532],
        "PR-AUC": [0.6450, 0.6696]
    })

        # --------------------------------------------------
    # 2. SELECTED MODEL KPI CARDS
    # --------------------------------------------------

    st.subheader("Selected Model — Performance Overview")

    st.caption(
        "Key evaluation metrics for the selected customer churn prediction model."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Selected Model",
        value="Tuned Random Forest",
        help="Machine learning model selected based primarily on its cross-validation F1 score."
    )

    col2.metric(
        label="Test F1 Score",
        value="63.33%",
        help="Harmonic mean of precision and recall on the test dataset."
    )

    col3.metric(
        label="Test Recall",
        value="76.20%",
        help="Percentage of actual churned customers correctly identified by the model."
    )

    col4.metric(
        label="Decision Threshold",
        value="0.52",
        help="Customers with a predicted churn probability of 0.52 or higher are classified as likely to churn."
    )

    st.caption(
        "The selected model applies a 0.52 probability threshold. "
        "A higher recall helps identify more customers who may discontinue the service."
    )

    st.divider()
    # --------------------------------------------------
    # 3. INITIAL MODEL COMPARISON
    # --------------------------------------------------

    st.subheader("Initial Model Comparison")

    st.write(
        "Four baseline classifiers were evaluated to understand "
        "their performance before hyperparameter tuning."
    )

    st.dataframe(
        comparison_data.style.format({
            "Accuracy": "{:.2%}",
            "Precision": "{:.2%}",
            "Recall": "{:.2%}",
            "F1 Score": "{:.2%}",
            "ROC-AUC": "{:.4f}",
            "PR-AUC": "{:.4f}"
        }),
        width="stretch",
        hide_index=True
    )

    selected_metric = st.selectbox(
        "Select a metric to compare initial models",
        [
            "F1 Score",
            "Accuracy",
            "Precision",
            "Recall",
            "ROC-AUC",
            "PR-AUC"
        ],
        index=0,
        key="initial_model_metric"
    )

    fig_initial = px.bar(
        comparison_data,
        x="Model",
        y=selected_metric,
        color="Model",
        text=selected_metric,
        title=f"Initial Model Comparison — {selected_metric}"
    )

    
    # Dynamic formatting based on selected metric
    if selected_metric in ["Accuracy", "Precision", "Recall", "F1 Score"]:
        metric_text_template = "%{text:.2%}"
    else:
        metric_text_template = "%{text:.4f}"

    fig_initial.update_traces(
        texttemplate=metric_text_template,
        textposition="outside"
    )


    fig_initial.update_layout(
        yaxis_title=selected_metric,
        xaxis_title="Machine Learning Model",
        yaxis_range=[0, 1.12],
        showlegend=False
    )

    st.plotly_chart(
        fig_initial,
        width="stretch"
    )

    st.divider()

    # --------------------------------------------------
    # 4. CROSS-VALIDATION COMPARISON
    # --------------------------------------------------

    st.subheader("Tuned Models — 5-Fold Cross-Validation")

    st.write(
        "Cross-validation helps evaluate model consistency "
        "across multiple stratified data splits."
    )

    st.dataframe(
        cv_data.style.format({
            "Tuned Random Forest": "{:.4f}",
            "Tuned Logistic Regression": "{:.4f}"
        }),
        width="stretch",
        hide_index=True
    )

    cv_metric = st.selectbox(
        "Select cross-validation metric",
        [
            "F1 Score",
            "Accuracy",
            "Precision",
            "Recall",
            "ROC-AUC",
            "PR-AUC"
        ],
        index=0,
        key="cv_model_metric"
    )

    selected_cv = cv_data[
        cv_data["Metric"] == cv_metric
    ]

    cv_comparison = pd.DataFrame({
        "Model": [
            "Tuned Random Forest",
            "Tuned Logistic Regression"
        ],
        "Score": [
            selected_cv["Tuned Random Forest"].iloc[0],
            selected_cv["Tuned Logistic Regression"].iloc[0]
        ]
    })

        # --------------------------------------------------
    # CROSS-VALIDATION COMPARISON CHART
    # --------------------------------------------------

    fig_cv = px.bar(
        cv_comparison,
        x="Model",
        y="Score",
        color="Model",
        text="Score",
        title=f"5-Fold Cross-Validation — {cv_metric}",
        hover_data={
            "Model": True,
            "Score": ":.4f"
        }
    )

    # Dynamic metric formatting
    if cv_metric in [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ]:
        cv_text_template = "%{text:.2%}"
        cv_axis_format = ".0%"
    else:
        cv_text_template = "%{text:.4f}"
        cv_axis_format = ".3f"

    fig_cv.update_traces(
        texttemplate=cv_text_template,
        textposition="outside",
        cliponaxis=False
    )

    fig_cv.update_layout(
        xaxis_title="Tuned Machine Learning Model",
        yaxis_title=cv_metric,
        yaxis=dict(
            range=[0, 1.12],
            tickformat=cv_axis_format
        ),
        showlegend=False,
        height=420,
        margin=dict(
            l=30,
            r=30,
            t=70,
            b=60
        ),
        title_x=0.02,
        hoverlabel=dict(
            namelength=-1
        )
    )

    st.plotly_chart(
        fig_cv,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )

    st.info(
        "Tuned Random Forest achieved a cross-validation F1-score "
        "of 0.6490, compared with 0.6419 for Tuned Logistic Regression."
    )

    st.caption(
        "All values represent mean scores across 5 stratified "
        "cross-validation folds."
    )

    st.divider()

    # --------------------------------------------------
    # 5. TEST SET EVALUATION
    # --------------------------------------------------

    st.subheader("Test Set Performance")

    st.write(
        "The following results compare the tuned models "
        "on the available test dataset."
    )

    st.dataframe(
        test_data.style.format({
            "Accuracy": "{:.2%}",
            "Precision": "{:.2%}",
            "Recall": "{:.2%}",
            "F1 Score": "{:.2%}",
            "ROC-AUC": "{:.4f}",
            "PR-AUC": "{:.4f}"
        }),
        width="stretch",
        hide_index=True
    )

        # --------------------------------------------------
    # TEST SET PERFORMANCE COMPARISON CHART
    # --------------------------------------------------

    test_comparison_long = test_data.melt(
        id_vars=["Model"],
        value_vars=[
            "Precision",
            "Recall",
            "F1 Score"
        ],
        var_name="Metric",
        value_name="Score"
    )

    fig_test = px.bar(
        test_comparison_long,
        x="Model",
        y="Score",
        color="Metric",
        barmode="group",
        text="Score",
        title="Test Set — Precision, Recall and F1 Score",
        hover_data={
            "Model": True,
            "Metric": True,
            "Score": ":.4f"
        },
        category_orders={
            "Metric": [
                "Precision",
                "Recall",
                "F1 Score"
            ]
        }
    )

    fig_test.update_traces(
        texttemplate="%{text:.2%}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Metric: %{fullData.name}<br>"
            "Score: %{y:.2%}"
            "<extra></extra>"
        )
    )

    fig_test.update_layout(
        xaxis_title="Tuned Machine Learning Model",
        yaxis_title="Performance Score",
        yaxis=dict(
            range=[0, 1.12],
            tickformat=".0%"
        ),
        legend_title="Evaluation Metric",
        height=450,
        margin=dict(
            l=30,
            r=30,
            t=75,
            b=65
        ),
        title_x=0.02,
        hoverlabel=dict(
            namelength=-1
        )
    )

    st.plotly_chart(
        fig_test,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )

    st.divider()

    # --------------------------------------------------
    # 6. CONFUSION MATRIX
    # --------------------------------------------------

    st.subheader("Confusion Matrix — Tuned Random Forest")

    st.caption(
        "Classification results at the selected probability threshold of 0.52."
    )

    confusion_matrix = pd.DataFrame(
        [[794, 241], [89, 285]],
        index=["Actual No Churn", "Actual Churn"],
        columns=["Predicted No Churn", "Predicted Churn"]
    )

        # --------------------------------------------------
    # CONFUSION MATRIX VISUALIZATION
    # --------------------------------------------------

    fig_cm = px.imshow(
        confusion_matrix,
        text_auto=",",
        color_continuous_scale="Blues",
        aspect="auto",
        labels={
            "x": "Predicted Class",
            "y": "Actual Class",
            "color": "Customer Count"
        },
        title="Tuned Random Forest — Classification Results"
    )

    fig_cm.update_traces(
        textfont=dict(
            size=20
        ),
        hovertemplate=(
            "Actual: %{y}<br>"
            "Predicted: %{x}<br>"
            "Customers: %{z:,}"
            "<extra></extra>"
        )
    )

    fig_cm.update_layout(
        xaxis_title="Predicted Customer Category",
        yaxis_title="Actual Customer Category",
        height=430,
        title_x=0.02,
        margin=dict(
            l=30,
            r=30,
            t=75,
            b=65
        ),
        coloraxis_colorbar=dict(
            title="Customers"
        ),
        hoverlabel=dict(
            namelength=-1
        )
    )

    fig_cm.update_xaxes(
        side="bottom"
    )

    st.plotly_chart(
        fig_cm,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )

    # Confusion matrix interpretation

    tn, fp, fn, tp = 794, 241, 89, 285

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("True Negatives", f"{tn:,}")
    col2.metric("False Positives", f"{fp:,}")
    col3.metric("False Negatives", f"{fn:,}")
    col4.metric("True Positives", f"{tp:,}")

    st.markdown("**Understanding the classification results:**")

    st.markdown(
        f"""
        - **True Positives ({tp}):** Actual churn customers correctly identified.
        - **True Negatives ({tn}):** Customers correctly identified as non-churn.
        - **False Positives ({fp}):** Non-churn customers incorrectly flagged as churn risks.
        - **False Negatives ({fn}):** Actual churn customers missed by the model.
        """
    )

    st.warning(
        "False negatives are particularly important in churn prediction "
        "because these are customers who may leave without being identified "
        "by the retention team."
    )

    st.divider()

        # --------------------------------------------------
    # 7. BUSINESS INTERPRETATION
    # --------------------------------------------------

    st.subheader("Business Interpretation")

    st.caption(
        "Translate model predictions into actionable "
        "customer retention insights."
    )

    churn_identification_rate = tp / (tp + fn)
    flagged_customer_precision = tp / (tp + fp)
    missed_churn_rate = fn / (tp + fn)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Churn Identification Rate",
        f"{churn_identification_rate:.2%}",
        help="Share of actual churn customers correctly identified."
    )

    col2.metric(
        "Flagged Customer Precision",
        f"{flagged_customer_precision:.2%}",
        help="Share of customers predicted as churn who actually churned."
    )

    col3.metric(
        "Missed Churn Rate",
        f"{missed_churn_rate:.2%}",
        help="Share of actual churn customers missed by the model."
    )

    st.markdown("### Business Insights")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        st.info(
            "**Customer Identification**\n\n"
            "The model identifies approximately 76% "
            "of actual churn customers."
        )

        st.info(
            "**Retention Opportunities**\n\n"
            "The retention team can prioritize flagged "
            "customers for further investigation."
        )

    with insight_col2:
        st.warning(
            "**False Positive Risk**\n\n"
            "Around 46% of flagged customers did not "
            "actually churn in the test dataset."
        )

        st.warning(
            "**Missed Customer Risk**\n\n"
            "Approximately 24% of actual churn customers "
            "were not identified."
        )

    st.caption(
        "These findings describe model classification outcomes "
        "and should not be interpreted as guaranteed business results."
    )

    st.divider()

    # --------------------------------------------------
    # 8. MODEL SELECTION SUMMARY
    # --------------------------------------------------

    st.subheader("Final Model Selection")

    st.caption(
        "Summary of the selected model and its configuration."
    )

    selection_col1, selection_col2 = st.columns(2)

    with selection_col1:

        st.markdown("### Selected Model")

        st.title("Random Forest")

        st.metric(
            "5-Fold CV F1 Score",
            "64.90%",
            help="Mean F1 score across five stratified cross-validation folds."
        )

        st.metric(
            "Test F1 Score",
            "63.33%",
            help="F1 score on the available test dataset."
        )

        st.metric(
            "Test Recall",
            "76.20%",
            help="Share of actual churn customers correctly identified."
        )

    with selection_col2:

        st.markdown("### Model Configuration")

        config_data = pd.DataFrame({
            "Parameter": [
                "Decision Threshold",
                "Number of Trees",
                "Maximum Depth",
                "Minimum Samples per Leaf",
                "Class Weight"
            ],
            "Value": [
                "0.52",
                "250",
                "10",
                "2",
                "Balanced"
            ]
        })

        st.dataframe(
            config_data,
            width="stretch",
            hide_index=True
        )

    st.success(
        "Tuned Random Forest was selected primarily because "
        "it achieved the highest 5-fold cross-validation "
        "F1-score among the tuned models."
    )

    st.warning(
        "Evaluation limitation: The test dataset was used in "
        "earlier model comparisons. Therefore, the reported "
        "test results should not be treated as a completely "
        "untouched final performance estimate."
    )

    st.caption(
        "Model performance metrics describe predictive performance "
        "and do not establish causal relationships between customer "
        "attributes and churn."
    )



elif selected_page == "Churn Prediction":

    st.title("Customer Churn Intelligence")
    st.caption(
        "AI-powered customer risk assessment and batch churn prediction "
        "using a tuned Random Forest classification model."
    )

    # --------------------------------------------------
    # 1. LOAD MODEL AND METADATA
    # --------------------------------------------------

    try:
        model, metadata = load_artifacts()
        threshold = float(metadata["decision_threshold"])

        st.success(
            f"Prediction Engine Active | Tuned Random Forest | "
            f"Decision Threshold: {threshold:.2f}"
        )

        with st.expander("View Model Configuration"):
            config_col1, config_col2, config_col3 = st.columns(3)

            config_col1.metric("Model", "Random Forest")
            config_col2.metric("Decision Threshold", f"{threshold:.2f}")
            config_col3.metric(
                "Positive Class",
                metadata.get("positive_class_meaning", "Churn = Yes")
            )

            st.caption(
                "The saved preprocessing and classification pipeline "
                "is used for all predictions."
            )

    except Exception as error:
        st.error(f"Unable to load prediction model: {error}")
        st.stop()

    st.divider()

    # --------------------------------------------------
    # 2. CSV UPLOAD
    # --------------------------------------------------

    st.subheader("Batch Customer Prediction")

    st.write(
        "Upload a customer CSV file to identify potential churn risks "
        "and prioritize retention opportunities."
    )

    uploaded_file = st.file_uploader(
        "Choose Customer CSV File",
        type=["csv"],
        help=(
            "The CSV must contain all 19 model input features. "
            "The churn target column is not required."
        ),
        key="churn_csv_uploader"
    )

    # --------------------------------------------------
    # 3. FILE TRACKING AND VALIDATION
    # --------------------------------------------------

    if uploaded_file is not None:

        file_hash = hashlib.sha256(
            uploaded_file.getvalue()
        ).hexdigest()

        previous_hash = st.session_state.get(
            "uploaded_file_hash"
        )

        if file_hash != previous_hash:

            st.session_state.pop("churn_results", None)
            st.session_state.pop("churn_results_file_hash", None)

            st.session_state["uploaded_file_hash"] = file_hash

        try:
            uploaded_file.seek(0)
            uploaded_df = pd.read_csv(uploaded_file)

            if uploaded_df.empty:

                st.warning(
                    "The uploaded CSV does not contain any customer records."
                )

            else:

                expected_features = list(model.feature_names_in_)

                missing_features = [
                    col for col in expected_features
                    if col not in uploaded_df.columns
                ]

                st.subheader("Upload Summary")

                summary_col1, summary_col2, summary_col3 = st.columns(3)

                summary_col1.metric(
                    "Uploaded Records",
                    f"{len(uploaded_df):,}"
                )

                summary_col2.metric(
                    "Available Columns",
                    f"{len(uploaded_df.columns):,}"
                )

                summary_col3.metric(
                    "Duplicate Records",
                    f"{uploaded_df.duplicated().sum():,}"
                )

                st.subheader("Customer Data Preview")

                st.dataframe(
                    uploaded_df.head(10),
                    width="stretch",
                    hide_index=True
                )

                if missing_features:

                    st.error(
                        "The uploaded file is missing required model features:"
                    )

                    st.write(", ".join(missing_features))

                    st.info(
                        "Please add all required columns and upload "
                        "the corrected CSV file."
                    )

                else:

                    # ------------------------------------------
                    # NUMERICAL VALIDATION
                    # ------------------------------------------

                    numerical_columns = [
                        "Tenure Months",
                        "Monthly Charges",
                        "Total Charges"
                    ]

                    invalid_columns = {}
                    validated_df = uploaded_df.copy()

                    for column in numerical_columns:

                        numeric_values = pd.to_numeric(
                            validated_df[column],
                            errors="coerce"
                        )

                        invalid_mask = (
                            numeric_values.isna()
                            | numeric_values.isin([
                                float("inf"),
                                float("-inf")
                            ])
                        )

                        if invalid_mask.any():

                            invalid_columns[column] = (
                                invalid_mask[invalid_mask].index + 2
                            ).tolist()

                        else:

                            validated_df[column] = numeric_values

                    if not invalid_columns:

                        # Additional domain validation
                        invalid_domain = {}

                        if (
                            (validated_df["Tenure Months"] < 0).any()
                            or (validated_df["Tenure Months"] > 72).any()
                        ):
                            invalid_domain["Tenure Months"] = (
                                "Expected values between 0 and 72."
                            )

                        for column in [
                            "Monthly Charges",
                            "Total Charges"
                        ]:
                            if (validated_df[column] < 0).any():
                                invalid_domain[column] = (
                                    "Negative charges are not valid."
                                )

                        if invalid_domain:

                            st.error(
                                "Some numerical values are outside "
                                "the expected business ranges."
                            )

                            for column, message in invalid_domain.items():
                                st.write(f"**{column}:** {message}")

                    if invalid_columns:

                        st.error(
                            "Missing or invalid numerical values detected."
                        )

                        for column, rows in invalid_columns.items():

                            st.write(
                                f"**{column} — CSV row(s):** {rows[:20]}"
                            )

                        st.warning(
                            "Please correct these values before "
                            "generating predictions."
                        )

                    elif not invalid_domain:

                        st.success(
                            "All required features and numerical "
                            "validations passed."
                        )

                        duplicate_count = uploaded_df.duplicated().sum()

                        if duplicate_count > 0:

                            st.warning(
                                f"{duplicate_count} duplicate records found. "
                                "They have not been automatically removed."
                            )

                        # ------------------------------------------
                        # GENERATE PREDICTIONS
                        # ------------------------------------------

                        if st.button(
                            "Generate Churn Predictions",
                            type="primary",
                            width="stretch",
                            key="generate_churn_predictions"
                        ):

                            try:

                                with st.spinner(
                                    "Analyzing customer records..."
                                ):

                                    results = predict_dataframe(
                                        validated_df,
                                        model,
                                        metadata
                                    )

                                    results = results.copy()

                                    def classify_risk(probability):
                                        if probability < threshold:
                                            return "Low"
                                        elif probability < 0.70:
                                            return "Medium"
                                        elif probability < 0.80:
                                            return "High"
                                        else:
                                            return "Very High"


                                    results["Risk_Category"] = results["Churn_Probability"].apply(
                                        classify_risk
                                    )

                                    st.session_state[
                                        "churn_results"
                                    ] = results

                                    st.session_state[
                                        "churn_results_file_hash"
                                    ] = file_hash

                                st.success(
                                    "Customer churn predictions generated successfully!"
                                )

                            except Exception as error:

                                st.error(
                                    f"Prediction generation failed: {error}"
                                )

        except Exception as error:

            st.error(
                f"Unable to read or process the uploaded CSV: {error}"
            )

    else:

        st.session_state.pop("churn_results", None)
        st.session_state.pop("churn_results_file_hash", None)
        st.session_state.pop("uploaded_file_hash", None)

        st.info(
            "Upload a customer CSV file to begin churn risk analysis."
        )

    # --------------------------------------------------
    # 4. DISPLAY PREDICTION RESULTS
    # --------------------------------------------------

    if (
        uploaded_file is not None
        and "churn_results" in st.session_state
        and st.session_state.get("churn_results_file_hash")
        == st.session_state.get("uploaded_file_hash")
    ):

        results = st.session_state["churn_results"].copy()

        st.divider()
        st.header("Prediction Results")

        total_customers = len(results)

        churn_count = (
            results["Predicted_Label"] == "Churn"
        ).sum()

        retained_count = (
            results["Predicted_Label"] == "No Churn"
        ).sum()

        churn_percentage = (
            churn_count / total_customers * 100
            if total_customers else 0
        )

        high_risk_count = results["Risk_Category"].isin(
            ["High", "Very High"]
        ).sum()

        very_high_risk_count = (
            results["Risk_Category"] == "Very High"
        ).sum()

        
        # ------------------------------------------
        # KPI CARDS
        # ------------------------------------------

        st.subheader("Prediction Executive Summary")

        st.caption(
            "Overview of customer churn predictions and "
            "risk distribution generated by the selected model."
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            label="Total Customers Analysed",
            value=f"{total_customers:,}",
            help="Total number of customer records processed by the prediction model."
        )

        col2.metric(
            label="Predicted Churn",
            value=f"{churn_count:,}",
            help="Number of customers classified as likely to discontinue the service."
        )

        col3.metric(
            label="Predicted No Churn",
            value=f"{retained_count:,}",
            help="Number of customers classified as likely to continue using the service."
        )

        col4.metric(
            label="Predicted Churn Share",
            value=f"{churn_percentage:.2f}%",
            help="Percentage of analysed customers predicted to churn."
        )

        st.markdown("#### Customer Risk Distribution")

        risk_col1, risk_col2, risk_col3 = st.columns(3)

        risk_col1.metric(
            label="High / Very High Risk",
            value=f"{high_risk_count:,}",
            help="Total customers classified into High or Very High risk categories."
        )

        risk_col2.metric(
            label="Very High Risk",
            value=f"{very_high_risk_count:,}",
            help="Customers with a predicted churn probability of 80% or higher."
        )

        risk_col3.metric(
            label="Decision Threshold",
            value=f"{threshold:.2f}",
            help="Probability cutoff used by the model to classify customers as Churn or No Churn."
        )

        st.divider()


        # ------------------------------------------
        # RISK DISTRIBUTION
        # ------------------------------------------

        st.subheader("Customer Risk Analysis")

        left, right = st.columns(2)

        risk_order = [
            "Low",
            "Medium",
            "High",
            "Very High"
        ]

        risk_distribution = (
            results["Risk_Category"]
            .value_counts()
            .reindex(risk_order, fill_value=0)
            .rename_axis("Risk Category")
            .reset_index(name="Customers")
        )

        with left:

            st.markdown("**Risk Category Distribution**")

            fig_risk = px.bar(
                risk_distribution,
                x="Risk Category",
                y="Customers",
                color="Risk Category",
                category_orders={
                    "Risk Category": risk_order
                },
                color_discrete_map={
                    "Low": "#16A34A",
                    "Medium": "#EAB308",
                    "High": "#F97316",
                    "Very High": "#DC2626"
                },
                text="Customers"
            )

            fig_risk.update_layout(
                showlegend=False,
                xaxis_title="Customer Risk Level",
                yaxis_title="Number of Customers"
            )

            st.plotly_chart(
                fig_risk,
                width="stretch"
            )

        with right:

            st.markdown("**Prediction Distribution**")

            distribution = (
                results["Predicted_Label"]
                .value_counts()
                .rename_axis("Prediction")
                .reset_index(name="Customers")
            )

            fig_distribution = px.pie(
                distribution,
                names="Prediction",
                values="Customers",
                hole=0.55,
                color="Prediction",
                color_discrete_map={
                    "Churn": "#EF4444",
                    "No Churn": "#2563EB"
                }
            )

            fig_distribution.update_traces(
                textposition="inside",
                textinfo="percent+label"
            )

            st.plotly_chart(
                fig_distribution,
                width="stretch"
            )

        # ------------------------------------------
        # CHURN PROBABILITY DISTRIBUTION
        # ------------------------------------------

        st.subheader("Churn Probability Distribution")

        fig_probability = px.histogram(
            results,
            x="Churn_Probability",
            nbins=25,
            color_discrete_sequence=["#2563EB"],
            labels={
                "Churn_Probability": "Predicted Churn Probability"
            }
        )

        fig_probability.add_vline(
            x=threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Decision Threshold: {threshold:.2f}"
        )

        fig_probability.update_layout(
            xaxis_title="Churn Probability",
            yaxis_title="Number of Customers"
        )

        st.plotly_chart(
            fig_probability,
            width="stretch"
        )

        st.caption(
            "Probabilities are model outputs, not guaranteed "
            "individual customer churn outcomes."
        )

        st.divider()

        # ------------------------------------------
        # RETENTION PRIORITY LIST
        # ------------------------------------------

        st.subheader("Retention Priority — Highest Risk Customers")

        priority_df = results[
            results["Risk_Category"].isin(
                ["High", "Very High"]
            )
        ].sort_values(
            "Churn_Probability",
            ascending=False
        )

        if not priority_df.empty:

            priority_columns = [
                col for col in [
                    "CustomerID",
                    "Contract",
                    "Tenure Months",
                    "Monthly Charges",
                    "Churn_Probability",
                    "Predicted_Label",
                    "Risk_Category"
                ]
                if col in priority_df.columns
            ]

            priority_display = priority_df[
                priority_columns
            ].head(10).copy()

            priority_display["Churn_Probability"] = (
                priority_display["Churn_Probability"] * 100
            ).round(2)

            st.dataframe(
                priority_display,
                width="stretch",
                hide_index=True
            )

            st.caption(
                "These are the first 10 customers prioritized by "
                "predicted churn probability, not confirmed churn cases."
            )

        else:

            st.info(
                "No customers were classified as High or Very High risk "
                "in this uploaded batch."
            )

        st.divider()

        # ------------------------------------------
        # CUSTOMER-LEVEL RESULTS AND FILTERS
        # ------------------------------------------

        st.subheader("Customer-Level Prediction Explorer")

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:

            risk_filter = st.multiselect(
                "Filter by Risk Category",
                options=risk_order,
                default=risk_order,
                key="prediction_risk_filter"
            )

        with filter_col2:

            label_filter = st.multiselect(
                "Filter by Prediction",
                options=["Churn", "No Churn"],
                default=["Churn", "No Churn"],
                key="prediction_label_filter"
            )

        filtered_results = results[
            results["Risk_Category"].isin(risk_filter)
            & results["Predicted_Label"].isin(label_filter)
        ].copy()

        display_results = filtered_results.copy()

        display_results["Churn_Probability"] = (
            display_results["Churn_Probability"] * 100
        ).round(2)

        st.caption(
            f"Showing {len(filtered_results):,} of "
            f"{total_customers:,} customer records."
        )

        st.dataframe(
            display_results,
            width="stretch",
            hide_index=True
        )

        st.divider()

        # ------------------------------------------
        # DOWNLOAD REPORTS
        # ------------------------------------------

        st.subheader("Download Prediction Reports")

        download_col1, download_col2 = st.columns(2)

        complete_csv = results.to_csv(
            index=False
        ).encode("utf-8")

        priority_csv = priority_df.to_csv(
            index=False
        ).encode("utf-8")

        with download_col1:

            st.download_button(
                label="Download Complete Prediction Report",
                data=complete_csv,
                file_name="customer_churn_predictions.csv",
                mime="text/csv",
                width="stretch",
                type="primary",
                key="download_complete_churn_report"
            )

        with download_col2:

            st.download_button(
                label="Download High-Risk Customer Report",
                data=priority_csv,
                file_name="high_risk_customers.csv",
                mime="text/csv",
                width="stretch",
                key="download_high_risk_report"
            )

        st.caption(
            f"Model decision threshold: {threshold:.2f}. "
            "Risk categories are business-facing probability bands: "
            "Low = below threshold, Medium = threshold to below 70%, "
            "High = 70% to below 80%, Very High = 80% or above. "
            "These risk bands are configurable and are not separately "
            "trained or calibrated model outputs."
        )
