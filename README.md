Credit Risk Analyzer 

An AI-powered credit risk analysis system built using Python (Flask), Machine Learning, and SQLite.
It evaluates a user’s financial profile and predicts loan eligibility using both rule-based scoring and a Logistic Regression ML model.

⸻

Live Demo

Coming soon (deployment in progress)

⸻

Features
	•	Rule-Based Risk Engine
Evaluates financial health using Debt-to-Income ratio, expenses, and credit score
	•	Machine Learning Model
Logistic Regression model trained on realistic synthetic financial data
	•	Explainable AI
Provides clear, factor-by-factor explanations for each decision
	•	Smart Recommendations
Personalized suggestions to improve loan approval chances
	•	Analytics Dashboard
Visual insights powered by Chart.js
	•	History Tracking
Stores and retrieves past analyses using SQLite

⸻

Tech Stack
	•	Backend: Python 3.11+, Flask
	•	Machine Learning: scikit-learn, NumPy, Pandas
	•	Frontend: HTML, CSS, JavaScript, Chart.js
	•	Database: SQLite

⸻

Project Structure

credit_risk_analyzer/
├── app.py                  # Flask app (routes + APIs)
├── services/
│   ├── risk_engine.py      # Rule-based scoring logic
│   └── ml_model.py         # ML model
├── models/
│   └── database.py         # Database handling
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   └── history.html
├── requirements.txt
└── README.md


⸻

Setup & Run

# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

Open in browser:
http://localhost:5000

⸻

API Endpoints

Method	Endpoint	Description
POST	/api/analyze	Perform risk analysis
GET	/api/history	Get all records
GET	/api/history/	Get specific record
GET	/api/stats	Get analytics


⸻

Sample Request

{
  "salary": 75000,
  "existing_loans": 15000,
  "monthly_expenses": 30000,
  "credit_score": 720,
  "employment_type": "salaried"
}


⸻

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

Scoring Logic

Rule-Based Score (0–100, higher = safer)

The system evaluates:
	•	Debt-to-Income Ratio
	•	Expense Ratio
	•	Credit Score
	•	Net Disposable Income
	•	Employment Stability

⸻

Machine Learning
	•	Model: Logistic Regression
	•	Data: 2,000 synthetic financial profiles
	•	Output: Risk category + probability

⸻

Key Highlights
	•	Combines finance logic + machine learning
	•	Provides transparent decision-making
	•	Designed as a real-world fintech prototype

⸻

Author

Raj Kumar Gurrapu
https://github.com/gurrapurajkumar99

⸻

 If you like this project, consider giving it a star!


⸻
