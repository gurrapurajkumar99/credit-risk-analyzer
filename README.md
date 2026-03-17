# Credit Risk Analyzer 🏦

An intelligent credit risk scoring system built with Python (Flask), SQLite, and scikit-learn.

## Features
- Rule-based risk scoring engine (debt-to-income, expense ratio, credit score weight)
- Logistic Regression ML model comparison
- Explainable AI — factor-by-factor breakdown
- Smart personalized recommendations
- Analytics dashboard with Chart.js visualizations
- Full analysis history with SQLite persistence

## Tech Stack
- **Backend**: Python 3.11+, Flask 3.0
- **ML**: scikit-learn (Logistic Regression), NumPy, Pandas
- **Frontend**: Vanilla JS, HTML5, CSS3, Chart.js
- **Database**: SQLite

## Project Structure
```
credit_risk_analyzer/
├── app.py                  # Flask application, routes
├── services/
│   ├── risk_engine.py      # Rule-based scoring engine
│   └── ml_model.py         # Logistic Regression classifier
├── models/
│   └── database.py         # SQLite ORM layer
├── templates/
│   ├── index.html          # Analyzer form + results
│   ├── dashboard.html      # Analytics dashboard
│   └── history.html        # History table
├── requirements.txt
└── README.md
```

## Setup & Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
# http://localhost:5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze` | Run risk analysis |
| GET | `/api/history` | Get all past analyses |
| GET | `/api/history/<id>` | Get specific analysis |
| GET | `/api/stats` | Aggregate statistics |

### POST /api/analyze — Request Body
```json
{
  "salary": 75000,
  "existing_loans": 15000,
  "monthly_expenses": 30000,
  "credit_score": 720,
  "employment_type": "salaried"
}
```

### Response
```json
{
  "risk_score": 28,
  "risk_category": "Low Risk",
  "factors": { "dti": 20.0, "expense_ratio": 40.0, ... },
  "explanations": [...],
  "suggestions": [...],
  "ml_prediction": {
    "risk_category": "Low Risk",
    "confidence": 91.2,
    "probabilities": { "Low Risk": 91.2, "Medium Risk": 7.1, "High Risk": 1.7 }
  }
}
```

## Scoring Algorithm

**Rule-Based Score (0–100, higher = riskier)**:
- Debt-to-Income Ratio: up to 40 points
- Expense Ratio: up to 30 points
- Credit Score: up to 35 points
- Net Disposable Income: up to 30 points
- Employment Type multiplier: 1.0× (salaried) / 1.25× (self-employed) / 1.6× (student)

**ML Model**: Logistic Regression trained on 2,000 synthetic profiles with realistic distributions across Low/Medium/High risk classes.
