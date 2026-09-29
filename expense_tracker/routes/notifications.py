from flask import Blueprint, render_template, session

from expense_tracker.models import Notification
from expense_tracker.routes import login_required


notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/notifications")
@login_required
def notifications_page():
    user_id = session.get("user_id")
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    return render_template("notifications.html", notifications=notifications)
