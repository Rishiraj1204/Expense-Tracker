from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from expense_tracker.models import Category, db
from expense_tracker.routes import login_required


categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/categories")
@login_required
def list_categories():
    user_id = session.get("user_id")
    categories = Category.query.filter_by(user_id=user_id).order_by(Category.name.asc()).all()
    return render_template("categories.html", categories=categories)


@categories_bp.route("/categories/add", methods=["POST"])
@login_required
def add_category():
    user_id = session.get("user_id")
    name = request.form.get("name", "").strip()
    category_type = request.form.get("type", "Expense")

    if not name:
        flash("Category name is required.", "error")
        return redirect(url_for("categories.list_categories"))

    existing = Category.query.filter_by(user_id=user_id, name=name).first()
    if existing:
        flash("Category already exists.", "error")
        return redirect(url_for("categories.list_categories"))

    category = Category(user_id=user_id, name=name, type=category_type)
    db.session.add(category)
    db.session.commit()
    flash("Category added successfully.", "success")
    return redirect(url_for("categories.list_categories"))
