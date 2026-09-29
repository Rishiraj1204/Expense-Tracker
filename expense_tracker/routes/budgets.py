from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from expense_tracker.models import Budget, Category, Expense, db
from expense_tracker.routes import login_required


budgets_bp = Blueprint("budgets", __name__)


@budgets_bp.route("/budget", methods=["GET", "POST"])
@login_required
def budget_page():
    user_id = session.get("user_id")
    categories = Category.query.filter_by(user_id=user_id).order_by(Category.name.asc()).all()

    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        amount = request.form.get("amount", type=float)
        month = request.form.get("month", type=int)
        year = request.form.get("year", type=int)

        if not amount or amount <= 0:
            flash("Budget amount must be greater than zero.", "error")
            return render_template("budget.html", categories=categories, budgets=Budget.query.filter_by(user_id=user_id).all())

        if category_id:
            existing = Budget.query.filter_by(user_id=user_id, category_id=category_id, month=month, year=year).first()
            if existing:
                existing.amount = amount
            else:
                db.session.add(Budget(user_id=user_id, category_id=category_id, amount=amount, month=month, year=year))
        else:
            existing = Budget.query.filter_by(user_id=user_id, category_id=None, month=month, year=year).first()
            if existing:
                existing.amount = amount
            else:
                db.session.add(Budget(user_id=user_id, category_id=None, amount=amount, month=month, year=year))

        db.session.commit()
        flash("Budget saved successfully.", "success")
        return redirect(url_for("budgets.budget_page"))

    budgets = Budget.query.filter_by(user_id=user_id).order_by(Budget.year.desc(), Budget.month.desc()).all()
    budget_summary = []

    for budget in budgets:
        spent = 0.0
        if budget.category_id:
            spent = sum(expense.amount for expense in Expense.query.filter_by(user_id=user_id, category_id=budget.category_id).all())
        else:
            spent = sum(expense.amount for expense in Expense.query.filter_by(user_id=user_id).all())

        utilization = (spent / budget.amount * 100) if budget.amount else 0
        budget_summary.append(
            {
                "budget": budget,
                "spent": spent,
                "remaining": budget.amount - spent,
                "utilization": utilization,
                "status": "OVER BUDGET" if utilization >= 100 else "CRITICAL" if utilization >= 85 else "WARNING" if utilization >= 70 else "NORMAL",
            }
        )

    return render_template("budget.html", categories=categories, budgets=budget_summary, now=datetime.now())
