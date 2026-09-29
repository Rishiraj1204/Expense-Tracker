from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from expense_tracker.models import User, db
from expense_tracker.routes import login_required


profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def profile():
    user_id = session.get("user_id")
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)


@profile_bp.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    user_id = session.get("user_id")
    user = User.query.get_or_404(user_id)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")

    if not name or not email:
        flash("Name and email are required.", "error")
        return redirect(url_for("profile.profile"))

    if email != user.email:
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email is already in use.", "error")
            return redirect(url_for("profile.profile"))

    if new_password:
        if not current_password or not check_password_hash(user.password_hash, current_password):
            flash("Current password is invalid.", "error")
            return redirect(url_for("profile.profile"))
        if len(new_password) < 6:
            flash("New password must be at least 6 characters long.", "error")
            return redirect(url_for("profile.profile"))
        user.password_hash = generate_password_hash(new_password)

    user.name = name
    user.email = email
    db.session.commit()
    flash("Profile updated successfully.", "success")
    return redirect(url_for("profile.profile"))
