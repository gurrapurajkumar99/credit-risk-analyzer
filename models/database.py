from pathlib import Path
import sqlite3
from datetime import datetime
import os

DEFAULT_DB_PATH = (
    Path('/tmp/credit_risk.db')
    if os.environ.get('VERCEL')
    else Path(__file__).resolve().parent.parent / 'credit_risk.db'
)

DB_PATH = Path(os.environ.get('CREDIT_RISK_DB', DEFAULT_DB_PATH))

class Database:
    def __init__(self):
        self._init_db()

    def _get_conn(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    salary REAL,
                    existing_loans REAL,
                    monthly_expenses REAL,
                    credit_score INTEGER,
                    employment_type TEXT,
                    risk_score INTEGER,
                    risk_category TEXT,
                    ml_risk_category TEXT,
                    created_at TEXT
                )
            ''')

    def save_analysis(self, data):
        with self._get_conn() as conn:
            cur = conn.execute('''
                INSERT INTO analyses
                (salary, existing_loans, monthly_expenses, credit_score, employment_type,
                 risk_score, risk_category, ml_risk_category, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['salary'], data['existing_loans'], data['monthly_expenses'],
                data['credit_score'], data['employment_type'], data['risk_score'],
                data['risk_category'], data['ml_risk_category'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            return cur.lastrowid

    def get_all(self):
        with self._get_conn() as conn:
            rows = conn.execute('SELECT * FROM analyses ORDER BY created_at DESC LIMIT 50').fetchall()
            return [dict(r) for r in rows]

    def get_by_id(self, record_id):
        with self._get_conn() as conn:
            row = conn.execute('SELECT * FROM analyses WHERE id = ?', (record_id,)).fetchone()
            return dict(row) if row else None

    def get_stats(self):
        with self._get_conn() as conn:
            total = conn.execute('SELECT COUNT(*) as c FROM analyses').fetchone()['c']
            by_cat = conn.execute('''
                SELECT risk_category, COUNT(*) as count FROM analyses GROUP BY risk_category
            ''').fetchall()
            avg_score = conn.execute('SELECT AVG(risk_score) as avg FROM analyses').fetchone()['avg']
            avg_credit = conn.execute('SELECT AVG(credit_score) as avg FROM analyses').fetchone()['avg']
            avg_salary = conn.execute('SELECT AVG(salary) as avg FROM analyses').fetchone()['avg']
            agreement = conn.execute('''
                SELECT
                    SUM(CASE WHEN risk_category = ml_risk_category THEN 1 ELSE 0 END) as matched,
                    COUNT(*) as total
                FROM analyses
            ''').fetchone()
            latest = conn.execute('''
                SELECT id, risk_score, risk_category, ml_risk_category, created_at
                FROM analyses
                ORDER BY created_at DESC
                LIMIT 1
            ''').fetchone()

            matched = agreement['matched'] or 0
            agreement_total = agreement['total'] or 0

            return {
                'total': total,
                'by_category': {r['risk_category']: r['count'] for r in by_cat},
                'average_score': round(avg_score, 1) if avg_score else 0,
                'average_credit_score': round(avg_credit, 1) if avg_credit else 0,
                'average_salary': round(avg_salary, 2) if avg_salary else 0,
                'model_agreement_rate': round((matched / agreement_total) * 100, 1) if agreement_total else 0,
                'latest_analysis': dict(latest) if latest else None
            }
