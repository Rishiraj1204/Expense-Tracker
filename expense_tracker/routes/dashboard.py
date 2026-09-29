from flask import Blueprint, render_template, session

from expense_tracker.routes import login_required
from expense_tracker.services.analytics_service import get_dashboard_data


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    user_id = session.get("user_id")
    data = get_dashboard_data(user_id)
    return render_template("dashboard.html", **data)
