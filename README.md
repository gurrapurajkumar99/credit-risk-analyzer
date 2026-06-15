
AI-Based Credit Risk Analyzer

An AI-powered Credit Risk Analysis System built using Python, Flask, SQLite, and Machine Learning. The application evaluates a user’s financial profile, predicts credit risk levels, and provides explainable recommendations to support informed financial decision-making.

Live Demo

🌐 Live Website: https://credit-risk-analyzer-pied.vercel.app/

🔗 GitHub Repository: https://github.com/gurrapurajkumar99/credit-risk-analyzer

⸻

Project Overview

Credit Risk Analyzer is a fintech-focused web application that combines traditional financial risk assessment techniques with Machine Learning to evaluate loan eligibility and borrower risk.

The system analyzes financial information such as salary, loan obligations, expenses, credit score, and employment type to generate a risk score and classify users into:

* Low Risk
* Medium Risk
* High Risk

The platform also provides transparent explanations and actionable recommendations to improve financial health.

⸻

Key Features

Financial Risk Assessment

* Debt-to-Income (DTI) Analysis
* Expense Ratio Analysis
* Credit Score Evaluation
* Net Disposable Income Calculation
* Employment Stability Assessment

Machine Learning Prediction

* Logistic Regression Classification Model
* Risk Category Prediction
* Confidence Score Analysis
* Probability Distribution Across Risk Levels

Explainable AI

* Factor-wise Risk Breakdown
* Human-readable Explanations
* Personalized Recommendations
* Transparent Decision Logic

Web Application Features

* Real-time Risk Analysis
* Input Validation and Error Handling
* Analysis History Tracking
* SQLite Data Persistence
* REST API Architecture
* Responsive User Interface

⸻

Tech Stack

Backend

* Python
* Flask
* Flask-CORS

Machine Learning

* Scikit-learn
* NumPy
* Pandas
* Logistic Regression

Database

* SQLite

Frontend

* HTML5
* CSS3
* JavaScript
* Chart.js

Deployment

* Vercel
* GitHub

⸻

Project Structure

credit_risk_analyzer/
│
├── app.py
├── models/
│   └── database.py
│
├── services/
│   ├── risk_engine.py
│   └── ml_model.py
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   └── history.html
│
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md

System Workflow

User Financial Data
↓
Input Validation
↓
Rule-Based Risk Engine
↓
Machine Learning Prediction
↓
Risk Classification
↓
Recommendation Generation
↓
Database Storage
↓
Results Dashboard

⸻

API Endpoints

Method	Endpoint	Description
GET	/health	Health Check
POST	/api/analyze	Run Risk Analysis
GET	/api/history	Retrieve Analysis History
GET	/api/history/{id}	Retrieve Specific Analysis
GET	/api/stats	Dashboard Statistics

⸻

Sample Request

{
  "salary": 75000,
  "existing_loans": 15000,
  "monthly_expenses": 30000,
  "credit_score": 720,
  "employment_type": "salaried"
}

Sample Response

{
  "risk_score": 82,
  "risk_category": "Low Risk",
  "ml_prediction": {
    "risk_category": "Low Risk",
    "confidence": 91.2
  }
}

⸻

Risk Evaluation Parameters

The system evaluates the following financial factors:

* Debt-to-Income Ratio
* Expense Ratio
* Credit Score
* Net Disposable Income
* Employment Type

Risk Categories

Score Range	Category
70 - 100	Low Risk
40 - 69	Medium Risk
0 - 39	High Risk

⸻

Key Skills Demonstrated

* Python Development
* Flask Web Development
* REST API Development
* Machine Learning Fundamentals
* Data Validation
* Explainable AI
* SQLite Database Management
* Software Testing and Debugging
* Git & GitHub
* FinTech Application Development

⸻

Future Enhancements

* User Authentication & Authorization
* PostgreSQL Database Integration
* Real-world Financial Dataset Training
* Advanced ML Models (XGBoost, Random Forest)
* Loan Approval Workflow
* Admin Dashboard
* Cloud Deployment
* Model Monitoring and Analytics

⸻

Resume Highlights

* Built an AI-powered Credit Risk Analyzer using Python, Flask, SQLite, and Machine Learning.
* Developed a rule-based scoring engine using financial risk metrics.
* Integrated Logistic Regression for borrower risk classification.
* Designed REST APIs for real-time analysis and history management.
* Implemented Explainable AI to provide transparent decision-making.
* Deployed a live fintech web application accessible through the web.

⸻

Author

Raj Kumar Gurrapu

GitHub: https://github.com/gurrapurajkumar99

LinkedIn: https://linkedin.com/in/rajkumargurrapu

