from collections import defaultdict
from datetime import datetime

from expense_tracker.models import Expense


def aggregate_by_period(user_id, period):
    expenses = Expense.query.filter_by(user_id=user_id).all()
    aggregates = defaultdict(float)

    for expense in expenses:
        if period == "day":
            key = expense.expense_date.isoformat()
        elif period == "week":
            iso_year, iso_week, _ = expense.expense_date.isocalendar()
            key = f"{iso_year}-W{iso_week:02d}"
        elif period == "month":
            key = expense.expense_date.strftime("%Y-%m")
        else:
            key = str(expense.expense_date.year)

        aggregates[key] += expense.amount

    return dict(sorted(aggregates.items()))
