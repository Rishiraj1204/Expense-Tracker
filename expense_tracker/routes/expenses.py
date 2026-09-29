from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from expense_tracker.models import Category, Expense, db
from expense_tracker.routes import login_required


expenses_bp = Blueprint("expenses", __name__)


def _get_user_expenses(user_id):
    query = Expense.query.filter_by(user_id=user_id)
    search = request.args.get("search", "").strip()
    category_id = request.args.get("category_id", type=int)
    payment_method = request.args.get("payment_method", "")
    sort = request.args.get("sort", "date_desc")

    if search:
        query = query.filter(Expense.description.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if payment_method:
        query = query.filter(Expense.payment_method == payment_method)

    if sort == "amount_asc":
        query = query.order_by(Expense.amount.asc())
    elif sort == "amount_desc":
        query = query.order_by(Expense.amount.desc())
    elif sort == "date_asc":
        query = query.order_by(Expense.expense_date.asc())
    else:
        query = query.order_by(Expense.expense_date.desc())

    return query.all()


@expenses_bp.route("/expenses")
@login_required
def list_expenses():
    user_id = session.get("user_id")
    categories = Category.query.filter_by(user_id=user_id).order_by(Category.name.asc()).all()
    expenses = _get_user_expenses(user_id)
    return render_template(
        "expenses.html",
        expenses=expenses,
        categories=categories,
        payment_methods=["Cash", "UPI", "Debit Card", "Credit Card", "Bank Transfer", "Other"],
        selected_category_id=request.args.get("category_id", type=int),
        selected_payment_method=request.args.get("payment_method", ""),
        selected_sort=request.args.get("sort", "date_desc"),
        selected_search=request.args.get("search", ""),
    )


@expenses_bp.route("/expenses/add", methods=["GET", "POST"])
@login_required
def add_expense():
    user_id = session.get("user_id")
    categories = Category.query.filter_by(user_id=user_id).all()

    if request.method == "POST":
        amount = request.form.get("amount", type=float)
        category_id = request.form.get("category_id", type=int)
        description = request.form.get("description", "").strip()
        payment_method = request.form.get("payment_method", "")
        expense_date = request.form.get("expense_date", "")

        if not all([amount, category_id, description, payment_method, expense_date]):
            flash("Please fill in all fields.", "error")
            return render_template("add_expense.html", categories=categories)
        if amount <= 0:
            flash("Expense amount must be greater than zero.", "error")
            return render_template("add_expense.html", categories=categories)

        try:
            parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Please enter a valid date.", "error")
            return render_template("add_expense.html", categories=categories)

        expense = Expense(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            description=description,
            payment_method=payment_method,
            expense_date=parsed_date,
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense added successfully.", "success")
        return redirect(url_for("expenses.list_expenses"))

    return render_template("add_expense.html", categories=categories)


@expenses_bp.route("/expenses/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_expense(id):
    user_id = session.get("user_id")
    expense = Expense.query.filter_by(id=id, user_id=user_id).first_or_404()
    categories = Category.query.filter_by(user_id=user_id).all()

    if request.method == "POST":
        amount = request.form.get("amount", type=float)
        category_id = request.form.get("category_id", type=int)
        description = request.form.get("description", "").strip()
        payment_method = request.form.get("payment_method", "")
        expense_date = request.form.get("expense_date", "")

        if not all([amount, category_id, description, payment_method, expense_date]):
            flash("Please fill in all fields.", "error")
            return render_template("edit_expense.html", expense=expense, categories=categories)
        if amount <= 0:
            flash("Expense amount must be greater than zero.", "error")
            return render_template("edit_expense.html", expense=expense, categories=categories)

        try:
            parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Please enter a valid date.", "error")
            return render_template("edit_expense.html", expense=expense, categories=categories)

        expense.amount = amount
        expense.category_id = category_id
        expense.description = description
        expense.payment_method = payment_method
        expense.expense_date = parsed_date
        db.session.commit()
        flash("Expense updated successfully.", "success")
        return redirect(url_for("expenses.list_expenses"))

    return render_template("edit_expense.html", expense=expense, categories=categories)


@expenses_bp.route("/expenses/delete/<int:id>")
@login_required
def delete_expense(id):
    user_id = session.get("user_id")
    expense = Expense.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully.", "success")
    return redirect(url_for("expenses.list_expenses"))
