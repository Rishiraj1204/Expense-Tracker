from flask import Blueprint, Response, render_template, session

from expense_tracker.models import Budget, Expense, Income
from expense_tracker.routes import login_required


reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports")
@login_required
def reports_page():
    user_id = session.get("user_id")
    incomes = Income.query.filter_by(user_id=user_id).all()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    budgets = Budget.query.filter_by(user_id=user_id).all()

    total_income = sum(item.amount for item in incomes)
    total_expense = sum(item.amount for item in expenses)
    balance = total_income - total_expense

    return render_template(
        "reports.html",
        incomes=incomes,
        expenses=expenses,
        budgets=budgets,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
    )


@reports_bp.route("/reports/export/csv")
@login_required
def export_csv():
    user_id = session.get("user_id")
    expenses = Expense.query.filter_by(user_id=user_id).all()
    output = []
    output.append("date,description,category,amount,payment_method\n")
    for expense in expenses:
        output.append(
            f"{expense.expense_date},{expense.description},{expense.category.name},{expense.amount},{expense.payment_method}\n"
        )

    return Response("".join(output), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=expenses.csv"})
