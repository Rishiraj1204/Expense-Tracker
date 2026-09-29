from collections import defaultdict


def detect_recurring_expenses(user_id):
    from expense_tracker.models import Expense

    try:
        expenses = Expense.query.filter_by(user_id=user_id).all()
    except RuntimeError:
        return []

    if len(expenses) < 2:
        return []

    grouped = defaultdict(list)
    for expense in expenses:
        grouped[(expense.category.name, round(expense.amount, 2))].append(expense)

    recurring = []
    for (category, amount), items in grouped.items():
        if len(items) >= 2:
            items_sorted = sorted(items, key=lambda item: item.expense_date)
            recurring.append({
                "category": category,
                "amount": amount,
                "count": len(items_sorted),
                "expenses": items_sorted,
            })

    return recurring
