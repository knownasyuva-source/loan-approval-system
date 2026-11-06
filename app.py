from datetime import datetime
import io
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Loan Approval Prediction System",
    page_icon="🏦",
    layout="wide",
)

# ---------------------------------------------------------
# INSTITUTIONAL FINTECH THEME (SUBTLE MESH GRID + FROSTED GLASS)
# ---------------------------------------------------------
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Professional Banking Terminal Background: Blueprint Mesh + Glow */
    .stApp {
        background-color: #0b1320;
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(37, 99, 235, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(16, 185, 129, 0.08) 0%, transparent 45%),
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px;
        color: #f1f5f9;
    }

    /* Glassmorphism Metric Card */
    .metric-card {
        background: rgba(18, 28, 48, 0.75);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35);
    }

    /* Header Container */
    .header-card {
        background: rgba(18, 28, 48, 0.85);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 1.2rem 1.8rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Status Badges */
    .status-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        padding: 5px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 0.6rem;
    }

    .badge-approved {
        background-color: rgba(34, 197, 94, 0.18);
        color: #4ade80;
        border: 1px solid rgba(74, 222, 128, 0.4);
    }

    .badge-rejected {
        background-color: rgba(239, 68, 68, 0.18);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.4);
    }

    .output-metric {
        font-size: 1.85rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
    }

    .output-label {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Primary Execution Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff;
        font-weight: 700;
        font-size: 0.95rem;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.35);
        transition: all 0.25s ease-in-out;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        border-color: #60a5fa;
        transform: translateY(-1px);
        box-shadow: 0 6px 24px rgba(37, 99, 235, 0.5);
    }

    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        color: #94a3b8;
        font-weight: 600;
        padding: 10px 18px;
    }

    .stTabs [aria-selected="true"] {
        color: #60a5fa !important;
        border-bottom: 2px solid #60a5fa;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# LOAD TRAINED MODEL & DATASET
# ---------------------------------------------------------
model = joblib.load("loan_model.pkl")


@st.cache_data
def load_data():
  df = pd.read_csv("loan_data.csv")
  df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())
  df["Credit_History"] = df["Credit_History"].fillna(
      df["Credit_History"].mode()[0]
  )
  df["Total_Income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
  return df


df_train = load_data()

# ---------------------------------------------------------
# APP HEADER
# ---------------------------------------------------------
st.markdown(
    """
<div class="header-card">
    <div>
        <h2 style="margin: 0; color: #ffffff; font-weight: 800; font-size: 1.6rem;">🏦 Loan Approval Prediction System</h2>
        <p style="margin: 0.3rem 0 0 0; color: #94a3b8; font-size: 0.9rem;">Machine Learning Credit Risk Assessment & Underwriting Platform</p>
    </div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; background: rgba(37, 99, 235, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); color: #93c5fd; padding: 6px 14px; border-radius: 20px;">
        ● MODEL ENGINE ACTIVE
    </div>
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs([
    "🎯 Individual Loan Evaluation",
    "📁 Batch Portfolio Processing",
    "📊 Model Analytics & Visualizations",
])

# =========================================================
# TAB 1: INDIVIDUAL LOAN PREDICTOR
# =========================================================
with tab1:
  st.markdown("#### **Applicant Profile & Financial Inputs**")

  col1, col2 = st.columns(2, gap="large")

  with col1:
    st.markdown("##### 👤 Applicant Demographics & Credit Status")
    credit_history = st.selectbox(
        "Credit History Bureau Status",
        [
            "Yes (No Prior Defaults)",
            "No (Prior Defaults / Delinquent Record)",
        ],
        index=0,
    )
    education = st.selectbox(
        "Education Qualification", ["Graduate", "Not Graduate"], index=0
    )
    property_area = st.selectbox(
        "Property Location Classification",
        ["Semiurban", "Urban", "Rural"],
        index=0,
    )
    tenure_years = st.slider("Requested Loan Tenure (Years)", 1, 30, 20)

  with col2:
    st.markdown("##### 💰 Income & Requested Facility Scale")
    applicant_income = st.number_input(
        "Applicant Monthly Income (₹)",
        min_value=1000,
        value=45000,
        step=2500,
    )
    coapplicant_income = st.number_input(
        "Co-Applicant Monthly Income (₹)",
        min_value=0,
        value=15000,
        step=2500,
    )
    loan_amount_inr = st.number_input(
        "Requested Loan Amount (₹)",
        min_value=10000,
        max_value=50000000,
        value=1500000,
        step=50000,
        help="Enter the exact amount in rupees (e.g. 1500000 for ₹15 Lakhs)",
    )
    annual_interest_rate = st.slider(
        "Assumed Annual Interest Rate (%)", 6.0, 15.0, 8.5, step=0.25
    )

  st.write("")
  evaluate_button = st.button(
      "Predict Loan Approval Status", type="primary", use_container_width=True
  )

  if evaluate_button:
    total_income = applicant_income + coapplicant_income
    loan_amount_k = loan_amount_inr / 1000.0
    loan_amount_log = np.log1p(loan_amount_k)

    credit_val = 1.0 if "Yes" in credit_history else 0.0
    edu_val = 0 if education == "Graduate" else 1
    area_map = {"Rural": 0, "Semiurban": 1, "Urban": 2}
    area_val = area_map[property_area]

    features = np.array(
        [[credit_val, edu_val, total_income, loan_amount_log, area_val]]
    )

    # Prediction
    prediction = model.predict(features)[0]
    prob_approved = model.predict_proba(features)[0][1] * 100

    # EMI & DTI calculation
    principal = float(loan_amount_inr)
    monthly_r = (annual_interest_rate / 12) / 100
    total_months = tenure_years * 12
    emi = (principal * monthly_r * ((1 + monthly_r) ** total_months)) / (
        ((1 + monthly_r) ** total_months) - 1
    )
    dti_ratio = (emi / total_income) * 100

    st.markdown("---")
    st.markdown("#### **Evaluation Results**")

    res_col1, res_col2 = st.columns(2, gap="large")

    with res_col1:
      if prediction == 1:
        st.markdown(
            f"""
                <div class="metric-card" style="border-left: 5px solid #22c55e;">
                    <span class="status-badge badge-approved">VERDICT: APPROVED</span>
                    <div class="output-metric" style="color: #4ade80;">Loan Sanctioned</div>
                    <div style="margin-top: 1rem; color: #cbd5e1; font-size: 0.9rem;">
                        <span class="output-label">Confidence Score:</span> <strong>{prob_approved:.1f}%</strong><br>
                        <span class="output-label">Architecture:</span> <strong>Random Forest Classifier</strong>
                    </div>
                </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        st.markdown(
            f"""
                <div class="metric-card" style="border-left: 5px solid #ef4444;">
                    <span class="status-badge badge-rejected">VERDICT: REJECTED</span>
                    <div class="output-metric" style="color: #f87171;">Loan Not Approved</div>
                    <div style="margin-top: 1rem; color: #cbd5e1; font-size: 0.9rem;">
                        <span class="output-label">Risk Probability:</span> <strong>{100 - prob_approved:.1f}%</strong><br>
                        <span class="output-label">Primary Factor:</span> <strong>{'Credit Defaults / Low Score' if credit_val == 0.0 else 'High Debt Burden / Loan Scale'}</strong>
                    </div>
                </div>
                """,
            unsafe_allow_html=True,
        )

    with res_col2:
      st.markdown(
          f"""
            <div class="metric-card">
                <span class="output-label">Repayment & Debt Burden Analysis</span>
                <div style="display: flex; justify-content: space-between; margin-top: 0.8rem;">
                    <div>
                        <div class="output-label">Estimated Monthly EMI</div>
                        <div class="output-metric">₹ {emi:,.0f}</div>
                    </div>
                    <div>
                        <div class="output-label">Debt-to-Income (DTI)</div>
                        <div class="output-metric" style="color: {'#f87171' if dti_ratio > 50 else '#4ade80'};">{dti_ratio:.1f}%</div>
                    </div>
                </div>
                <div style="margin-top: 0.8rem; font-size: 0.85rem; color: #cbd5e1;">
                    {'⚠️ <strong style="color: #fca5a5;">High DTI Alert:</strong> Monthly obligation exceeds 50% of income.' if dti_ratio > 50 else '💡 <strong style="color: #86efac;">Healthy Repayment:</strong> Monthly obligation is within standard limits (<50%).'}
                </div>
            </div>
            """,
          unsafe_allow_html=True,
      )

    # Counterfactual recommendations on rejection
    if prediction == 0:
      st.markdown("#### 💡 Prescriptive Counterfactual Recommendations:")
      suggested_changes = []

      # Loan reduction test
      for test_loan_k in [loan_amount_k * 0.7, loan_amount_k * 0.5]:
        if (
            model.predict(
                np.array([[
                    credit_val,
                    edu_val,
                    total_income,
                    np.log1p(test_loan_k),
                    area_val,
                ]])
            )[0]
            == 1
        ):
          suggested_changes.append(
              f"Right-size requested loan to **₹ {test_loan_k * 1000:,.0f}**."
          )
          break

      # Income enhancement test
      for extra in [15000, 30000]:
        if (
            model.predict(
                np.array([[
                    credit_val,
                    edu_val,
                    total_income + extra,
                    loan_amount_log,
                    area_val,
                ]])
            )[0]
            == 1
        ):
          suggested_changes.append(
              f"Add a co-applicant contributing at least **₹ {extra:,.0f}/month**."
          )
          break

      if credit_val == 0.0:
        suggested_changes.append(
            "Clear delinquent past obligations to restore a positive credit bureau record."
        )

      if suggested_changes:
        for s in suggested_changes:
          st.write(f"• {s}")
      else:
        st.write(
            "• Application requires manual underwriter review due to elevated risk parameters across multiple indicators."
        )

    # Download summary report
    report_text = f"""LOAN APPROVAL PREDICTION REPORT
--------------------------------------------------
Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Prediction Status: {'APPROVED' if prediction == 1 else 'REJECTED'}
Confidence Level: {prob_approved:.2f}%

APPLICANT PROFILE:
Total Monthly Income: Rs. {total_income:,.2f}
Education Qualification: {education}
Property Location: {property_area}
Credit History Status: {'Clear / No Defaults' if credit_val == 1.0 else 'Delinquent Records Found'}

LOAN FACILITY TERMS:
Requested Loan Principal: Rs. {loan_amount_inr:,.2f}
Tenure: {tenure_years} Years
Interest Rate: {annual_interest_rate}% p.a.
Estimated Monthly EMI: Rs. {emi:,.2f}
Debt-to-Income (DTI) Ratio: {dti_ratio:.2f}%
--------------------------------------------------"""

    st.download_button(
        "📄 Download Assessment Summary (.txt)",
        data=report_text,
        file_name=f"Loan_Assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
    )


# =========================================================
# TAB 2: BULK PORTFOLIO DATASET PROCESSING
# =========================================================
with tab2:
  st.subheader("Bulk Portfolio CSV Prediction")
  st.write(
      "Upload a CSV file containing multiple applicant records to evaluate their loan status simultaneously."
  )

  sample_df = pd.DataFrame({
      "ApplicantIncome": [55000, 28000, 75000, 18000],
      "CoapplicantIncome": [15000, 0, 30000, 0],
      "LoanAmount_Thousands": [220, 350, 150, 400],
      "Credit_History": [1.0, 0.0, 1.0, 0.0],
      "Education": ["Graduate", "Not Graduate", "Graduate", "Not Graduate"],
      "Property_Area": ["Urban", "Rural", "Semiurban", "Rural"],
  })

  st.download_button(
      "📥 Download Sample CSV Template",
      sample_df.to_csv(index=False),
      file_name="loan_batch_template.csv",
      mime="text/csv",
  )

  uploaded_file = st.file_uploader(
      "Upload CSV File", type=["csv"], key="batch_file"
  )

  if uploaded_file:
    b_df = pd.read_csv(uploaded_file)
    try:
      tot_inc = b_df["ApplicantIncome"] + b_df["CoapplicantIncome"]
      ln_log = np.log1p(b_df["LoanAmount_Thousands"])
      ed_val = b_df["Education"].map({"Graduate": 0, "Not Graduate": 1})
      cr_val = b_df["Credit_History"]
      ar_val = b_df["Property_Area"].map(
          {"Rural": 0, "Semiurban": 1, "Urban": 2}
      )

      b_matrix = np.column_stack((cr_val, ed_val, tot_inc, ln_log, ar_val))
      preds = model.predict(b_matrix)
      probs = model.predict_proba(b_matrix)[:, 1] * 100

      b_df["Prediction"] = np.where(preds == 1, "Approved", "Rejected")
      b_df["Confidence_%"] = np.round(probs, 2)

      m1, m2, m3 = st.columns(3)
      m1.metric("Total Records", len(b_df))
      m2.metric("Approved", int(np.sum(preds == 1)))
      m3.metric("Rejected", int(np.sum(preds == 0)))

      st.dataframe(b_df, use_container_width=True)

      st.download_button(
          "💾 Download Scored Results (.csv)",
          b_df.to_csv(index=False),
          file_name=f"Processed_Loan_Results_{datetime.now().strftime('%Y%m%d')}.csv",
          mime="text/csv",
      )
    except Exception as e:
      st.error(
          f"Column schema error: Ensure CSV columns match the template. ({e})"
      )


# =========================================================
# TAB 3: MODEL ANALYTICS & VISUALIZATIONS
# =========================================================
with tab3:
  st.subheader("Model Performance & Dataset Insights")

  col_m1, col_m2 = st.columns(2, gap="large")

  with col_m1:
    st.markdown("#### Feature Importance (Random Forest)")
    feature_names = [
        "Credit History",
        "Education",
        "Total Income",
        "Loan Amount",
        "Property Area",
    ]
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor("#0b1320")
    ax.set_facecolor("#121c30")

    ax.barh(
        range(len(sorted_idx)),
        importances[sorted_idx],
        color="#388bfd",
        edgecolor="#1d4ed8",
    )
    ax.set_yticks(range(len(sorted_idx)))
    ax.set_yticklabels([feature_names[i] for i in sorted_idx], color="#f1f5f9")
    ax.tick_params(colors="#94a3b8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#334155")
    ax.spines["bottom"].set_color("#334155")
    ax.set_xlabel("Relative Importance Score", color="#94a3b8")
    st.pyplot(fig)

  with col_m2:
    st.markdown("#### Algorithm Performance Comparison")
    b_df = pd.DataFrame({
        "Model": [
            "Random Forest",
            "Logistic Regression",
            "Decision Tree",
        ],
        "Accuracy (%)": [78.90, 76.40, 71.20],
        "F1-Score": [0.79, 0.75, 0.70],
    })
    st.dataframe(b_df, hide_index=True, use_container_width=True)

    fig2, ax2 = plt.subplots(figsize=(6, 2.7))
    fig2.patch.set_facecolor("#0b1320")
    ax2.set_facecolor("#121c30")
    sns.barplot(
        x="Model", y="Accuracy (%)", data=b_df, palette="Blues_r", ax=ax2
    )
    ax2.set_ylim(60, 90)
    ax2.tick_params(colors="#94a3b8")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_color("#334155")
    ax2.spines["bottom"].set_color("#334155")
    st.pyplot(fig2)