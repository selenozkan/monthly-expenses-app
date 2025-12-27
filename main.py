from flask.views import MethodView
from flask import Flask, render_template, request
from month_budget.budget import MonthlyBudget
from wtforms import Form, StringField, SubmitField


app = Flask(__name__)

class MonthlyBudgetPage(MethodView): # This class will respond to HTTP methods (GET, POST etc.). So flask will look for get() post() functions
    def get(self): # this IS the endpoint
        form = MonthlyBudgetForm()
        return render_template('index.html', form=form)

    def post(self):
        form = MonthlyBudgetForm(request.form)

        income_raw = (form.user_income.data or "").strip()
        period_raw = (form.user_period.data or "").strip()

        # If user submitted an empty form, just re-render cleanly (no results)
        if income_raw == "" and period_raw == "" and all(
                (a or "").strip() == "" for a in request.form.getlist("amount[]")):
            return render_template("index.html", form=MonthlyBudgetForm())

        # If income is missing/invalid, show a friendly message and stop
        try:
            income = float(income_raw)
        except ValueError:
            return render_template("index.html", form=form, error="Please enter a valid income (e.g. 2500).")

        if income <= 0:
            return render_template("index.html", form=form, error="Income must be greater than 0.")

        budget = MonthlyBudget(income, period_raw or "Unknown period")

        categories = request.form.getlist("category[]")
        amounts = request.form.getlist("amount[]")

        for cat, amt in zip(categories, amounts):
            amt = (amt or "").strip()
            if amt == "":
                continue  # ignore empty rows
            budget.add_expense(cat, float(amt))

        return render_template(
            "index.html",
            form=form,
            period=budget.period,
            total_expense=budget.total_expenses(),
            remaining=budget.remaining(),
            savings_rate=budget.savings_rate(),
            breakdown=budget.percent_of_expense_by_category(),
        )


class MonthlyBudgetForm(Form):
    user_period = StringField('Month-Year' )
    user_income = StringField('Income €: ')
    button = SubmitField('Calculate')


app.add_url_rule("/", view_func=MonthlyBudgetPage.as_view("index"), methods=["GET", "POST"])

app.run(debug=True)