import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 1. Load dataset
df = pd.read_csv("loan_data.csv")

# 2. Impute missing values
df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].median())
df["Credit_History"] = df["Credit_History"].fillna(
    df["Credit_History"].mode()[0]
)
df = df.dropna()

# 3. Feature engineering
df["Total_Income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
df["LoanAmount_Log"] = np.log1p(df["LoanAmount"])

# 4. Encode categorical fields
le = LabelEncoder()
df["Education"] = le.fit_transform(df["Education"])  # Graduate: 0, Not: 1
df["Property_Area"] = le.fit_transform(
    df["Property_Area"]
)  # Rural: 0, Semiurban: 1, Urban: 2
df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

# 5. Define features (X) and target (y)
X = df[[
    "Credit_History",
    "Education",
    "Total_Income",
    "LoanAmount_Log",
    "Property_Area",
]]
y = df["Loan_Status"]

# 6. Train-test split (80-20 rule)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. Evaluate
y_pred = model.predict(X_test)
print("=" * 40)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("=" * 40)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# 9. Save the trained model
joblib.dump(model, "loan_model.pkl")
print("\n[SUCCESS] Model saved as 'loan_model.pkl'!")