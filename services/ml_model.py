import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class MLModel:
    """
    Logistic Regression-based credit risk classifier.
    Trained on synthetic data that mirrors realistic credit risk distributions.
    """

    def __init__(self):
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.scaler = StandardScaler()
        self.trained = False
        self.labels = ['Low Risk', 'Medium Risk', 'High Risk']
        self.employment_map = {'salaried': 0, 'self-employed': 1, 'student': 2}
        self.feature_names = [
            'monthly_salary',
            'existing_loan_emis',
            'monthly_expenses',
            'credit_score',
            'employment_type'
        ]
        self.training_summary = {
            'algorithm': 'Logistic Regression',
            'training_rows': 0,
            'accuracy': 0,
            'features': self.feature_names,
            'classes': self.labels,
            'trained': False
        }

    def _generate_training_data(self, n=2000):
        np.random.seed(42)
        data, labels = [], []

        # Low Risk profiles
        for _ in range(700):
            salary = np.random.uniform(60000, 200000)
            loans = np.random.uniform(0, salary * 0.25)
            expenses = np.random.uniform(salary * 0.2, salary * 0.45)
            credit = np.random.randint(720, 900)
            emp = np.random.choice([0, 1], p=[0.8, 0.2])
            data.append([salary, loans, expenses, credit, emp])
            labels.append(0)

        # Medium Risk profiles
        for _ in range(700):
            salary = np.random.uniform(25000, 100000)
            loans = np.random.uniform(salary * 0.2, salary * 0.5)
            expenses = np.random.uniform(salary * 0.4, salary * 0.65)
            credit = np.random.randint(580, 720)
            emp = np.random.choice([0, 1, 2], p=[0.5, 0.35, 0.15])
            data.append([salary, loans, expenses, credit, emp])
            labels.append(1)

        # High Risk profiles
        for _ in range(600):
            salary = np.random.uniform(10000, 60000)
            loans = np.random.uniform(salary * 0.45, salary * 0.9)
            expenses = np.random.uniform(salary * 0.55, salary * 0.95)
            credit = np.random.randint(300, 600)
            emp = np.random.choice([0, 1, 2], p=[0.3, 0.3, 0.4])
            data.append([salary, loans, expenses, credit, emp])
            labels.append(2)

        return np.array(data), np.array(labels)

    def train(self):
        X, y = self._generate_training_data()
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model.fit(X_train_scaled, y_train)
        predictions = self.model.predict(X_test_scaled)
        self.trained = True
        self.training_summary = {
            'algorithm': 'Logistic Regression',
            'training_rows': int(len(X_train)),
            'test_rows': int(len(X_test)),
            'accuracy': round(float(accuracy_score(y_test, predictions)) * 100, 1),
            'features': self.feature_names,
            'classes': self.labels,
            'trained': True
        }

    def ensure_trained(self):
        if not self.trained:
            self.train()

    def _encode_employment(self, employment_type):
        return self.employment_map.get(employment_type.lower(), 0)

    def predict(self, salary, existing_loans, monthly_expenses, credit_score, employment_type):
        self.ensure_trained()

        emp_encoded = self._encode_employment(employment_type)
        features = np.array([[salary, existing_loans, monthly_expenses, credit_score, emp_encoded]])
        features_scaled = self.scaler.transform(features)

        pred_class = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]

        return {
            'risk_category': self.labels[pred_class],
            'confidence': round(float(probabilities[pred_class]) * 100, 1),
            'probabilities': {
                'Low Risk': round(float(probabilities[0]) * 100, 1),
                'Medium Risk': round(float(probabilities[1]) * 100, 1),
                'High Risk': round(float(probabilities[2]) * 100, 1)
            }
        }

    def get_summary(self):
        return self.training_summary
