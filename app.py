from flask import Flask, render_template, request, jsonify
from services.risk_engine import RiskEngine
from services.ml_model import MLModel
from models.database import Database
from flask_cors import CORS
import os

# -----------------------------
# INIT APP
# -----------------------------
app = Flask(__name__)
CORS(app)

db = Database()
risk_engine = RiskEngine()
ml_model = MLModel()

# Train ML model
try:
    ml_model.train()
    print("✅ ML Model trained successfully")
except Exception as e:
    print("❌ ML training failed:", e)

# -----------------------------
# ROUTES (PAGES)
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/history')
def history():
    return render_template('history.html')


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


# -----------------------------
# MAIN ANALYSIS API
# -----------------------------
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    # -------- VALIDATION --------
    if not data:
        return jsonify({'error': 'No data received'}), 400

    try:
        salary = float(data.get('salary', 0))
        existing_loans = float(data.get('existing_loans', 0))
        monthly_expenses = float(data.get('monthly_expenses', 0))
        credit_score = int(data.get('credit_score', 0))
        employment_type = str(data.get('employment_type', '')).lower()
    except:
        return jsonify({'error': 'Invalid input types'}), 400

    if salary <= 0:
        return jsonify({'error': 'Salary must be greater than 0'}), 400

    if existing_loans < 0 or monthly_expenses < 0:
        return jsonify({'error': 'Loans/expenses cannot be negative'}), 400

    if not (300 <= credit_score <= 900):
        return jsonify({'error': 'Credit score must be 300–900'}), 400

    if employment_type not in ['salaried', 'self-employed', 'student']:
        return jsonify({'error': 'Invalid employment type'}), 400

    # -------- RULE ENGINE --------
    result = risk_engine.analyze(
        salary,
        existing_loans,
        monthly_expenses,
        credit_score,
        employment_type
    )

    # -------- ML MODEL --------
    try:
        ml_result = ml_model.predict(
            salary,
            existing_loans,
            monthly_expenses,
            credit_score,
            employment_type
        )
    except Exception as e:
        print("ML Error:", e)
        ml_result = {
            'risk_category': 'Unavailable',
            'confidence': 0,
            'probabilities': {}
        }

    result['ml_prediction'] = ml_result

    # -------- SAVE DATABASE --------
    try:
        record_id = db.save_analysis({
            'salary': salary,
            'existing_loans': existing_loans,
            'monthly_expenses': monthly_expenses,
            'credit_score': credit_score,
            'employment_type': employment_type,
            'risk_score': result['risk_score'],
            'risk_category': result['risk_category'],
            'ml_risk_category': ml_result['risk_category']
        })
        result['record_id'] = record_id
    except Exception as e:
        print("DB Error:", e)
        result['record_id'] = None

    return jsonify(result)


# -----------------------------
# HISTORY APIs
# -----------------------------
@app.route('/api/history')
def get_history():
    try:
        return jsonify(db.get_all())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/<int:record_id>')
def get_record(record_id):
    record = db.get_by_id(record_id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record)


@app.route('/api/stats')
def get_stats():
    try:
        return jsonify(db.get_stats())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == '__main__':
    import os

    port = 5001   # 🔥 force change (no env confusion)

    print(f"🚀 Starting Flask server on port {port}...")
    print(f"👉 Open: http://127.0.0.1:{port}/")

    app.run(debug=True, host='127.0.0.1', port=port)