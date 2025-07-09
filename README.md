# Risk Tolerance Prediction App 🧠📈

A web-based application that predicts an individual's risk tolerance based on a short questionnaire and recommends a personalized investment portfolio.

---

## 🔍 Overview

This project combines **machine learning** and **financial modeling** to help users assess their investment risk profile. The model is trained using real financial data (SCF 2022 - Federal Reserve), and users are provided with investment portfolio suggestions based on their risk score.

---

## 🛠️ Tech Stack

- **Python** (pandas, scikit-learn, matplotlib)
- **Django** for web framework
- **SQLite** as database
- **Bootstrap** for basic UI styling
- **Google Colab** used for ML experimentation
- **Jupyter Notebook** for model development & evaluation

---

## 📊 Machine Learning

- **Model Type**: Random Forest Regressor (Risk Score ∈ [0, 1])
- **Features**:
  - Income Level
  - Savings
  - Age
  - Investment Knowledge
  - Questionnaire Responses
- **Output**:
  - Risk Tolerance Score (0 = Low Risk, 1 = High Risk)
  - Portfolio allocation suggestion:
    - % Stocks
    - % Bonds
    - % Cash

---

## 📁 Files in This Repo

| File | Description |
|------|-------------|
| `RISK_TOLERANCE_MODEL.ipynb` | ML model training & evaluation |
| `questionnaire/` | Django app with frontend forms |
| `SCFP2022.csv` | Training dataset |
| `DataMiningReport.pdf` | Academic report/documentation |
| `requirements.txt` | Python package requirements |
| `manage.py` | Django app runner |

---

## 🧪 Example Output

> User fills in 5 questions → Model outputs:
> - Risk Score: 0.73
> - Suggested Portfolio: 80% Stocks, 15% Bonds, 5% Cash

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/pkappaa/Risk_Tolerance_Prediction-App.git
cd Risk_Tolerance_Prediction-App
pip install -r requirements.txt
python manage.py runserver
