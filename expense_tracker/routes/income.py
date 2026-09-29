from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from expense_tracker.models import Income, db
from expense_tracker.routes import login_required


income_bp = Blueprint("income", __name__)


@income_bp.route("/income")
@login_required
def list_income():
    user_id = session.get("user_id")
    incomes = Income.query.filter_by(user_id=user_id).order_by(Income.income_date.desc()).all()
    return render_template("income.html", incomes=incomes)


@income_bp.route("/income/add", methods=["GET", "POST"])
@login_required
def add_income():
    if request.method == "POST":
        user_id = session.get("user_id")
        source = request.form.get("source", "").strip()
        amount = request.form.get("amount", type=float)
        description = request.form.get("description", "").strip()
        income_date = request.form.get("income_date", "")

        if not all([source, amount, description, income_date]):
            flash("Please fill in all fields.", "error")
            return render_template("add_income.html")
        if amount <= 0:
            flash("Income amount must be greater than zero.", "error")
            return render_template("add_income.html")

        try:
            parsed_date = datetime.strptime(income_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Please enter a valid date.", "error")
            return render_template("add_income.html")

        income = Income(user_id=user_id, source=source, amount=amount, description=description, income_date=parsed_date)
        db.session.add(income)
        db.session.commit()
        flash("Income added successfully.", "success")
        return redirect(url_for("income.list_income"))

    return render_template("add_income.html")


@income_bp.route("/income/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_income(id):
    user_id = session.get("user_id")
    income = Income.query.filter_by(id=id, user_id=user_id).first_or_404()

    if request.method == "POST":
        source = request.form.get("source", "").strip()
        amount = request.form.get("amount", type=float)
        description = request.form.get("description", "").strip()
        income_date = request.form.get("income_date", "")

        if not all([source, amount, description, income_date]):
            flash("Please fill in all fields.", "error")
            return render_template("edit_income.html", income=income)
        if amount <= 0:
            flash("Income amount must be greater than zero.", "error")
            return render_template("edit_income.html", income=income)

        try:
            parsed_date = datetime.strptime(income_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Please enter a valid date.", "error")
            return render_template("edit_income.html", income=income)

        income.source = source
        income.amount = amount
        income.description = description
        income.income_date = parsed_date
        db.session.commit()
        flash("Income updated successfully.", "success")
        return redirect(url_for("income.list_income"))

    return render_template("edit_income.html", income=income)


@income_bp.route("/income/delete/<int:id>")
@login_required
def delete_income(id):
    user_id = session.get("user_id")
    income = Income.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(income)
    db.session.commit()
    flash("Income deleted successfully.", "success")
    return redirect(url_for("income.list_income"))
