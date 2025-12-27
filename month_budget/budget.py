class MonthlyBudget:
    def __init__(self, income, period):
        self.income = float(income)
        self.period = str(period)
        self.expenses = {
            "housing": 0.0,
            "food": 0.0,
            "transport": 0.0,
            "entertainment": 0.0,
            "health": 0.0,
            "extras": 0.0
        }

    def add_expense(self, category, amount):
        if category not in self.expenses:
            raise ValueError("Invalid expense category")
        self.expenses[category] += float(amount)

    def total_expenses(self):
        return sum(self.expenses.values())

    def remaining(self):
        return self.income - self.total_expenses()

    def savings_rate(self):
        if self.income <= 0 or self.remaining() <= 0:
            return 0
        return round((self.remaining() / self.income) * 100, 2)

    def percent_of_expense_by_category(self):
        total = self.total_expenses()
        if total == 0:
            return {cat: 0 for cat in self.expenses}
        return {cat: (value / total) * 100 for cat, value in self.expenses.items()}