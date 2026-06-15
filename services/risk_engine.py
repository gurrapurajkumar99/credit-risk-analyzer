class RiskEngine:
    """Bank-grade credit risk scoring engine with FOIR, DTI, expense, and explainability."""

    EMPLOYMENT_WEIGHTS = {
        'salaried': 10,
        'self-employed': 7,
        'student': 4
    }

    def analyze(self, salary, existing_loans, monthly_expenses, credit_score, employment_type):
        salary = max(float(salary), 1.0)
        existing_loans = max(float(existing_loans), 0.0)
        monthly_expenses = max(float(monthly_expenses), 0.0)
        credit_score = int(round(max(300, min(900, credit_score))))
        employment_type = str(employment_type).lower()
        employment_type = employment_type if employment_type in self.EMPLOYMENT_WEIGHTS else 'salaried'

        dti = existing_loans / salary
        expense_ratio = monthly_expenses / salary
        net_income = salary - existing_loans - monthly_expenses
        disposable_rate = max(0.0, net_income / salary)
        foir = (existing_loans + monthly_expenses) / salary

        credit_points = self._credit_score_points(credit_score)
        dti_points = self._dti_points(dti)
        foir_points = self._foir_points(foir)
        expense_points = self._expense_points(expense_ratio)
        disposable_points = self._disposable_points(disposable_rate)
        employment_points = self.EMPLOYMENT_WEIGHTS.get(employment_type, 7)

        rule_score = int(round(
            credit_points + dti_points + foir_points + expense_points + disposable_points + employment_points
        ))
        rule_score = max(0, min(100, rule_score))

        category = self._category_from_score(rule_score)
        approval_probability = self._approval_probability(rule_score, dti, foir)
        approval_label = self._approval_label(approval_probability)
        financial_health_score = int(round((rule_score * 0.7) + (approval_probability * 0.3)))
        loan_affordability = self._loan_affordability_score(foir, dti, disposable_rate)

        explanations = [
            self._build_explanation(
                'Credit Score',
                credit_score,
                self._impact_text(credit_points, 30),
                self._risk_level_from_credit(credit_score),
                self._recommend_credit_score(credit_score)
            ),
            self._build_explanation(
                'Debt-to-Income Ratio',
                f'{dti*100:.1f}%',
                self._impact_text(dti_points, 25),
                self._risk_level_from_dti(dti),
                self._recommend_dti(dti)
            ),
            self._build_explanation(
                'FOIR',
                f'{foir*100:.1f}%',
                self._impact_text(foir_points, 20),
                self._risk_level_from_foir(foir),
                self._recommend_foir(foir)
            ),
            self._build_explanation(
                'Expense Ratio',
                f'{expense_ratio*100:.1f}%',
                self._impact_text(expense_points, 10),
                self._risk_level_from_expense(expense_ratio),
                self._recommend_expense(expense_ratio)
            ),
            self._build_explanation(
                'Net Disposable Income',
                f'₹{net_income:,.0f}',
                self._impact_text(disposable_points, 10),
                self._risk_level_from_disposable(disposable_rate),
                self._recommend_disposable(disposable_rate)
            ),
            self._build_explanation(
                'Employment Type',
                employment_type.title(),
                self._impact_text(employment_points, 10),
                self._risk_level_from_employment(employment_type),
                self._recommend_employment(employment_type)
            )
        ]

        return {
            'risk_score': rule_score,
            'risk_category': category,
            'approval_probability': approval_probability,
            'approval_label': approval_label,
            'creditworthiness_index': rule_score,
            'financial_health_score': financial_health_score,
            'loan_affordability_score': loan_affordability,
            'dti': round(dti * 100, 1),
            'foir': round(foir * 100, 1),
            'expense_ratio': round(expense_ratio * 100, 1),
            'net_income': round(net_income, 2),
            'disposable_income': round(disposable_rate * 100, 1),
            'employment_type': employment_type,
            'credit_score': credit_score,
            'factors': {
                'credit_score': credit_score,
                'dti': round(dti * 100, 1),
                'foir': round(foir * 100, 1),
                'expense_ratio': round(expense_ratio * 100, 1),
                'disposable_rate': round(disposable_rate * 100, 1),
                'employment_type': employment_type,
            },
            'explanations': explanations,
            'recommendations': self._generate_recommendations(credit_score, dti, foir, expense_ratio, disposable_rate, employment_type),
            'status': self._risk_status(category)
        }

    def _credit_score_points(self, score):
        if score >= 780:
            return 30
        if score >= 720:
            return 25
        if score >= 650:
            return 18
        if score >= 600:
            return 10
        return 2

    def _dti_points(self, dti):
        if dti <= 0.25:
            return 25
        if dti <= 0.35:
            return 18
        if dti <= 0.45:
            return 10
        if dti <= 0.50:
            return 5
        return 0

    def _foir_points(self, foir):
        if foir <= 0.30:
            return 20
        if foir <= 0.40:
            return 15
        if foir <= 0.50:
            return 8
        if foir <= 0.60:
            return 4
        return 0

    def _expense_points(self, expense_ratio):
        if expense_ratio <= 0.35:
            return 10
        if expense_ratio <= 0.50:
            return 6
        if expense_ratio <= 0.60:
            return 3
        return 0

    def _disposable_points(self, disposable_rate):
        if disposable_rate >= 0.25:
            return 10
        if disposable_rate >= 0.15:
            return 7
        if disposable_rate >= 0.05:
            return 4
        return 0

    def _category_from_score(self, score):
        if score >= 85:
            return 'Excellent'
        if score >= 70:
            return 'Good'
        if score >= 55:
            return 'Moderate'
        if score >= 40:
            return 'High Risk'
        return 'Very High Risk'

    def _approval_probability(self, rule_score, dti, foir):
        base = rule_score
        if dti > 0.50 or foir > 0.60:
            base -= 15
        elif dti > 0.40 or foir > 0.50:
            base -= 8
        if base < 0:
            base = 0
        return min(100, int(base))

    def _approval_label(self, probability):
        if probability >= 90:
            return 'Excellent'
        if probability >= 75:
            return 'Good'
        if probability >= 60:
            return 'Moderate'
        return 'Risky'

    def _loan_affordability_score(self, foir, dti, disposable_rate):
        score = (1 - foir) * 55 + (1 - dti) * 30 + disposable_rate * 15
        return int(max(0, min(100, round(score))))

    def _risk_status(self, category):
        return {
            'Excellent': 'Strong',
            'Good': 'Healthy',
            'Moderate': 'Watchlist',
            'High Risk': 'Elevated Risk',
            'Very High Risk': 'Critical'
        }.get(category, 'Unknown')

    def _risk_level_from_credit(self, score):
        if score >= 720:
            return 'Low'
        if score >= 650:
            return 'Medium'
        return 'High'

    def _risk_level_from_dti(self, dti):
        if dti <= 0.30:
            return 'Low'
        if dti <= 0.45:
            return 'Medium'
        return 'High'

    def _risk_level_from_foir(self, foir):
        if foir <= 0.35:
            return 'Low'
        if foir <= 0.55:
            return 'Medium'
        return 'High'

    def _risk_level_from_expense(self, expense_ratio):
        if expense_ratio <= 0.35:
            return 'Low'
        if expense_ratio <= 0.50:
            return 'Medium'
        return 'High'

    def _risk_level_from_disposable(self, disposable_rate):
        if disposable_rate >= 0.25:
            return 'Low'
        if disposable_rate >= 0.10:
            return 'Medium'
        return 'High'

    def _risk_level_from_employment(self, employment_type):
        if employment_type == 'salaried':
            return 'Low'
        if employment_type == 'self-employed':
            return 'Medium'
        return 'High'

    def _impact_text(self, points, max_points):
        scaled = int(round((points / max_points) * 15)) if max_points else 0
        return f'{scaled:+d} points'

    def _build_explanation(self, factor, current_value, impact, risk_level, recommendation):
        return {
            'factor': factor,
            'current_value': current_value,
            'impact': impact,
            'risk_level': risk_level,
            'recommendation': recommendation
        }

    def _generate_recommendations(self, credit_score, dti, foir, expense_ratio, disposable_rate, employment_type):
        recs = []
        if credit_score < 700:
            recs.append({'icon': '📈', 'title': 'Improve CIBIL score', 'description': 'Pay bills on time and reduce credit utilization below 30%.', 'priority': 'high'})
        if dti > 0.40:
            recs.append({'icon': '🏦', 'title': 'Lower EMI burden', 'description': 'Refinance or prepay high-interest loans to reduce DTI.', 'priority': 'high'})
        if foir > 0.50:
            recs.append({'icon': '💳', 'title': 'Optimize fixed obligations', 'description': 'Reduce EMIs and monthly commitments to improve FOIR.', 'priority': 'high'})
        if expense_ratio > 0.45:
            recs.append({'icon': '💰', 'title': 'Cut discretionary spend', 'description': 'Reduce non-essential expenses to raise savings and affordability.', 'priority': 'medium'})
        if disposable_rate < 0.15:
            recs.append({'icon': '🛡️', 'title': 'Build an emergency fund', 'description': 'Keep at least 3 months of salary in liquid savings.', 'priority': 'medium'})
        if employment_type == 'student':
            recs.append({'icon': '🎓', 'title': 'Consider a guarantor', 'description': 'A guarantor or co-applicant can strengthen approval chances.', 'priority': 'medium'})
        if not recs:
            recs.append({'icon': '✅', 'title': 'Maintain your profile', 'description': 'Your credit profile is healthy; continue disciplined credit behavior.', 'priority': 'positive'})
        return recs

    def _recommend_credit_score(self, score):
        if score >= 780:
            return 'Maintain your excellent CIBIL profile and avoid new credit inquiries.'
        if score >= 720:
            return 'Continue timely payments and keep credit utilisation below 30%.'
        if score >= 650:
            return 'Boost your score above 700 by lowering debt and paying EMIs on schedule.'
        return 'Pay all dues promptly and reduce outstanding credit to raise your bureau score.'

    def _recommend_dti(self, dti):
        if dti <= 0.30:
            return 'DTI is strong. Keep new EMI commitments under 30% of income.'
        if dti <= 0.45:
            return 'Manage existing debt so DTI stays below 40% for better lender confidence.'
        return 'High DTI suggests repayment pressure. Reduce loans or increase income.'

    def _recommend_foir(self, foir):
        if foir <= 0.35:
            return 'FOIR is excellent. Your fixed obligations are well within bank limits.'
        if foir <= 0.55:
            return 'Lower fixed obligations to push FOIR below 50% for smoother approvals.'
        return 'High FOIR increases risk. Reduce EMIs and monthly commitments.'

    def _recommend_expense(self, expense_ratio):
        if expense_ratio <= 0.35:
            return 'Expenses are under control. Maintain a strong savings rate.'
        if expense_ratio <= 0.50:
            return 'Reduce discretionary spending to improve cashflow and approval strength.'
        return 'Expenses are high. Cut unnecessary costs and rebuild reserves.'

    def _recommend_disposable(self, disposable_rate):
        if disposable_rate >= 0.25:
            return 'Healthy disposable income. Keep saving and avoid new debt.'
        if disposable_rate >= 0.10:
            return 'Moderate disposable income. Add a buffer to handle surprises.'
        return 'Low disposable income. Increase savings or reduce expenses.'

    def _recommend_employment(self, employment_type):
        if employment_type == 'salaried':
            return 'Stable salaried income is viewed positively by lenders.'
        if employment_type == 'self-employed':
            return 'Maintain strong documentation and steady cashflow for self-employed lending.'
        return 'Students may need a guarantor for credit approval.'
