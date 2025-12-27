from budget import MonthlyBudget

user_income = input("Please enter your income: ")
user_period = input("Please enter the period (e.g. December 2025): ")

budget = MonthlyBudget(user_income, user_period)

print(f'Hello, lets calculate your monthly budget. For {budget.period}, your income is {budget.income}.')

while True:
    user_category = input('Choose a category (housing, food, transport, lifestyle, health, extras) '
        'or type "done": '
    ).strip().lower()
    if user_category == "done":
        break
    category_expense = input(f'Please enter how much you spent on category "{user_category}":' )
    budget.add_expense(user_category, float(category_expense))


total_expense = (budget.total_expenses())
print("Your total expense is:", total_expense)
print(f"Remaining {budget.remaining()}, which is about {budget.savings_rate()}% of the income.")
print("Breakdown of expenses by category:")
print(budget.percent_of_expense_by_category())