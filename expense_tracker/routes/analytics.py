from flask import Blueprint, render_template, session

from expense_tracker.analytics.anomaly import detect_anomalies
from expense_tracker.analytics.moving_average import calculate_moving_average
from expense_tracker.analytics.recurring import detect_recurring_expenses
from expense_tracker.analytics.time_series import aggregate_by_period
from expense_tracker.analytics.trends import analyse_trends
from expense_tracker.routes import login_required
from expense_tracker.services.analytics_service import get_analytics_data


analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
@login_required
def analytics_page():
    user_id = session.get("user_id")
    data = get_analytics_data(user_id)
    data["daily"] = aggregate_by_period(user_id, "day")
    data["weekly"] = aggregate_by_period(user_id, "week")
    data["monthly"] = aggregate_by_period(user_id, "month")
    data["yearly"] = aggregate_by_period(user_id, "year")
    data["moving_average"] = calculate_moving_average(data["expenses"])
    data["trend_analysis"] = analyse_trends(data["monthly"])
    data["anomalies"] = detect_anomalies(data["expenses"])
    data["recurring"] = detect_recurring_expenses(user_id)
    return render_template("analytics.html", **data)
