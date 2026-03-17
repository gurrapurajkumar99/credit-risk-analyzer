class RiskEngine:
    """
    Improved credit risk scoring engine (realistic + interview-ready)
    Score: 0–95 (higher = safer, NOT riskier)
    """

    EMPLOYMENT_WEIGHTS = {
        'salaried': 1.0,
        'self-employed': 0.9,
        'student': 0.75
    }

    def analyze(self, salary, existing_loans, monthly_expenses, credit_score, employment_type):
        factors = {}
        explanations = []
        score = 100  # start from best

        # -----------------------------
        # 1. Debt-to-Income Ratio (DTI)
        # -----------------------------
        dti = (existing_loans / salary) if salary > 0 else 1
        factors['dti'] = round(dti * 100, 2)

        if dti > 0.5:
            score -= 35
            severity = 'high'
            msg = 'High debt-to-income ratio — over 50% income used for loans.'
        elif dti > 0.35:
            score -= 20
            severity = 'medium'
            msg = 'Moderate debt burden affecting repayment capacity.'
        else:
            severity = 'low'
            msg = 'Healthy debt-to-income ratio.'

        explanations.append({
            'factor': 'Debt-to-Income Ratio',
            'value': f'{dti*100:.1f}%',
            'severity': severity,
            'message': msg
        })

        # -----------------------------
        # 2. Expense Ratio
        # -----------------------------
        expense_ratio = (monthly_expenses / salary) if salary > 0 else 1
        factors['expense_ratio'] = round(expense_ratio * 100, 2)

        if expense_ratio > 0.7:
            score -= 25
            severity = 'high'
            msg = 'Expenses too high — very low savings.'
        elif expense_ratio > 0.5:
            score -= 15
            severity = 'medium'
            msg = 'Spending is relatively high.'
        else:
            severity = 'low'
            msg = 'Good expense control.'

        explanations.append({
            'factor': 'Expense Ratio',
            'value': f'{expense_ratio*100:.1f}%',
            'severity': severity,
            'message': msg
        })

        # -----------------------------
        # 3. Credit Score
        # -----------------------------
        factors['credit_score'] = credit_score

        if credit_score < 580:
            score -= 30
            severity = 'high'
            msg = 'Poor credit history.'
        elif credit_score < 670:
            score -= 15
            severity = 'medium'
            msg = 'Average credit score.'
        elif credit_score < 740:
            score -= 5
            severity = 'low'
            msg = 'Good credit score.'
        else:
            score += 5
            severity = 'low'
            msg = 'Excellent credit score.'

        explanations.append({
            'factor': 'Credit Score',
            'value': str(credit_score),
            'severity': severity,
            'message': msg
        })

        # -----------------------------
        # 4. Net Income
        # -----------------------------
        net_income = salary - existing_loans - monthly_expenses
        factors['net_income'] = round(net_income, 2)

        if net_income < 0:
            score -= 30
            severity = 'high'
            msg = 'Negative net income.'
        elif net_income < salary * 0.1:
            score -= 15
            severity = 'medium'
            msg = 'Low disposable income.'
        else:
            severity = 'low'
            msg = 'Healthy savings.'

        explanations.append({
            'factor': 'Net Income',
            'value': f'₹{net_income:,.0f}',
            'severity': severity,
            'message': msg
        })

        # -----------------------------
        # 5. Employment
        # -----------------------------
        emp_weight = self.EMPLOYMENT_WEIGHTS.get(employment_type, 0.85)
        factors['employment_type'] = employment_type

        if employment_type == 'student':
            score -= 15
            severity = 'high'
            msg = 'No stable income.'
        elif employment_type == 'self-employed':
            score -= 5
            severity = 'medium'
            msg = 'Income variability risk.'
        else:
            severity = 'low'
            msg = 'Stable salaried income.'

        explanations.append({
            'factor': 'Employment Type',
            'value': employment_type,
            'severity': severity,
            'message': msg
        })

        # -----------------------------
        # FINAL SCORE CALCULATION (FIXED)
        # -----------------------------
        score = score * emp_weight

        # 🔥 Prevent unrealistic perfect scores
        if score > 90:
            score = 90 + (score % 5)  # slight variation

        score = max(0, min(95, int(score)))  # cap at 95

        # -----------------------------
        # CATEGORY
        # -----------------------------
        if score >= 70:
            category = 'Low Risk'
        elif score >= 40:
            category = 'Medium Risk'
        else:
            category = 'High Risk'

        suggestions = self._generate_suggestions(category)

        return {
            'risk_score': score,
            'risk_category': category,
            'factors': factors,
            'explanations': explanations,
            'suggestions': suggestions
        }

    # -----------------------------
    # Suggestions
    # -----------------------------
    def _generate_suggestions(self, category):
        if category == 'High Risk':
            return [
                {'icon': '📉', 'title': 'Reduce Expenses', 'description': 'Cut spending by 20%', 'priority': 'high'},
                {'icon': '🏦', 'title': 'Reduce Loans', 'description': 'Lower EMI burden', 'priority': 'high'},
                {'icon': '📊', 'title': 'Improve Credit Score', 'description': 'Pay bills on time', 'priority': 'high'}
            ]

        elif category == 'Medium Risk':
            return [
                {'icon': '📈', 'title': 'Improve Profile', 'description': 'Increase savings', 'priority': 'medium'},
                {'icon': '💰', 'title': 'Reduce Expenses', 'description': 'Target <50% expense ratio', 'priority': 'medium'}
            ]

        else:
            return [
                {'icon': '✅', 'title': 'Eligible for Loan', 'description': 'Strong profile', 'priority': 'positive'}
            ]