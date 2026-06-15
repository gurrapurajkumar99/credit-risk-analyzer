# AI-Based Credit Risk Analyzer

An explainable credit risk web application built with Python, Flask, SQLite, and scikit-learn. The project predicts Low, Medium, or High risk from a user's financial profile and explains the decision in language that non-technical stakeholders can understand.

## Main Motto

Make credit decisions fast, explainable, and accessible for non-technical stakeholders.

This project is designed as a fintech prototype for:

- Applicants who want to understand loan readiness before applying.
- Loan officers who need consistent risk screening and clear decision reasons.
- Risk managers who want dashboard-level insight into portfolio risk patterns.

## Live Demo

Deployment target: Render Free Web Service.

Live website: https://credit-risk-analyzer.onrender.com

After connecting the GitHub repository on Render, use:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Health check path: `/health`

The repo also includes `render.yaml` for blueprint-style setup.

## Features

- Rule-based scoring engine using debt-to-income ratio, FOIR, expense ratio, credit score, disposable income, and employment type.
- Machine learning comparision using Logistic Regression with probability scores and confidence.
- Approval probability and final decision engine for lender-style approval guidance.
- Explainable AI output with factor-by-factor reasoning and actionable recommendations.
- Smart recommendations to improve loan eligibility, affordability, and creditworthiness.
- Professional analytics dashboard with risk distribution, approval gauge, trends, and stakeholder context.
- History page with saved borrower evaluations, rule vs ML comparison, and decision tracking.
- SQLite persistence for demo history plus deployment-ready Flask configuration.

## Tech Stack

- Backend: Python, Flask
- Machine Learning: scikit-learn, NumPy
- Database: SQLite
- Frontend: HTML, CSS, JavaScript, Chart.js
- Deployment: Render / Gunicorn

## Project Structure

```text
credit_risk_analyzer/
├── app.py                  # Flask routes and APIs
├── models/
│   └── database.py         # SQLite storage layer
├── services/
│   ├── risk_engine.py      # Rule-based scoring logic
│   └── ml_model.py         # Logistic Regression classifier
├── templates/
│   ├── index.html          # Analyzer form and result page
│   ├── dashboard.html      # Analytics and stakeholder dashboard
│   └── history.html        # Saved analysis records
├── render.yaml             # Render deployment config
├── Procfile                # Gunicorn start command
├── runtime.txt             # Python version hint
├── requirements.txt
└── README.md
```

## Setup Locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Deployment health check |
| GET | `/api/project-info` | Motto, stakeholders, and login decision |
| GET | `/api/model-info` | ML algorithm, training rows, accuracy, and features |
| POST | `/api/analyze` | Run credit risk analysis |
| GET | `/api/history` | Get recent saved analyses |
| GET | `/api/history/<id>` | Get one saved analysis |
| GET | `/api/stats` | Dashboard aggregate metrics |

## Sample Request

```json
{
  "salary": 75000,
  "existing_loans": 15000,
  "monthly_expenses": 30000,
  "credit_score": 720,
  "employment_type": "salaried"
}
```

## Sample Response

```json
{
  "risk_score": 82,
  "risk_category": "Low Risk",
  "factors": {
    "dti": 20,
    "expense_ratio": 40,
    "credit_score": 720,
    "net_income": 30000,
    "employment_type": "salaried"
  },
  "ml_prediction": {
    "risk_category": "Low Risk",
    "confidence": 91.2
  }
}
```

## Scoring Logic

The rule-based score is a safety score from 0 to 100. Higher is safer.

- Low Risk: score >= 70
- Medium Risk: score >= 40 and < 70
- High Risk: score < 40

The scoring engine evaluates:

- Debt-to-income ratio
- Expense ratio
- Credit score
- Net disposable income
- Employment stability

## Machine Learning Approach

The ML model uses Logistic Regression because it is fast, interpretable, and suitable for a student/internship-level fintech prototype.

Features used:

- Monthly salary
- Existing monthly loan EMIs
- Monthly expenses
- Credit score
- Employment type

The model is trained on synthetic profiles because this public portfolio project should not include real private financial data.

## Is Login Required?

For this demo, login is intentionally not required.

Reason: the current application is a public analysis prototype. It does not store real identity documents, bank statements, or account-specific workflows.

In a production version, login would be added for:

- Borrower accounts
- Loan officer review queues
- Admin dashboards
- Audit logs
- Secure personal financial history

## Resume Alignment

Resume point:

> Built a credit risk prediction system using financial datasets with Low/Medium/High risk classification.

Project evidence:

- Rule engine and Logistic Regression both classify users into Low, Medium, or High risk.
- The API returns model confidence and probabilities for each class.

Resume point:

> Performed data cleaning, feature engineering, and generated explainable reports for non-technical stakeholders.

Project evidence:

- Inputs are validated and normalized before analysis.
- Financial ratios such as DTI, expense ratio, and disposable income act as engineered features.
- Results include plain-English explanations, factor severity, and recommendations.

## Interview Talking Points

- Why combine rules and ML?
  Rules are transparent and easy to explain. ML gives a second opinion and probability-based comparison.

- Why Logistic Regression?
  It is interpretable, efficient, and appropriate for classification with structured financial features.

- Why SQLite?
  SQLite is simple for a prototype and good for local/demo history. Production can move to PostgreSQL.

- Why no login?
  Auth is unnecessary for a public prototype. It becomes necessary when storing user-specific private financial data.

- What would you improve next?
  Add real anonymized datasets, PostgreSQL, user authentication, model monitoring, fairness checks, and loan officer approval workflows.

## Author

Raj Kumar Gurrapu  
GitHub: https://github.com/gurrapurajkumar99
