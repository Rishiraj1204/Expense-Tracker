from collections import defaultdict

from expense_tracker.models import Budget, Category, Expense, Income


def get_dashboard_data(user_id):
    expenses = Expense.query.filter_by(user_id=user_id).all()
    incomes = Income.query.filter_by(user_id=user_id).all()
    categories = Category.query.filter_by(user_id=user_id).all()
    budgets = Budget.query.filter_by(user_id=user_id).all()

    total_income = sum(item.amount for item in incomes)
    total_expenses = sum(item.amount for item in expenses)
    current_balance = total_income - total_expenses

    monthly_budget = sum(item.amount for item in budgets if item.category_id is None)
    budget_used = total_expenses
    remaining_budget = monthly_budget - budget_used

    category_map = defaultdict(float)
    for expense in expenses:
        category_map[expense.category.name] += expense.amount

    highest_spending_category = max(category_map.items(), key=lambda item: item[1], default=("None", 0))
    top_expense = max(expenses, key=lambda item: item.amount, default=None)

    recent_transactions = sorted(expenses, key=lambda item: item.expense_date, reverse=True)[:5]

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "current_balance": current_balance,
        "monthly_budget": monthly_budget,
        "budget_used": budget_used,
        "remaining_budget": remaining_budget,
        "recent_transactions": recent_transactions,
        "highest_spending_category": highest_spending_category,
        "top_expense": top_expense,
        "categories": categories,
        "expenses": expenses,
        "incomes": incomes,
        "budgets": budgets,
    }


def get_analytics_data(user_id):
    expenses = Expense.query.filter_by(user_id=user_id).all()
    incomes = Income.query.filter_by(user_id=user_id).all()

    total_spent = sum(item.amount for item in expenses)
    total_income = sum(item.amount for item in incomes)
    average_expense = total_spent / len(expenses) if expenses else 0
    highest_expense = max((item.amount for item in expenses), default=0)
    lowest_expense = min((item.amount for item in expenses), default=0)

    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense.category.name] += expense.amount

    expenses_sorted = sorted(expenses, key=lambda item: item.amount, reverse=True)
    top_k = expenses_sorted[:5]

    return {
        "expenses": expenses,
        "incomes": incomes,
        "total_spent": total_spent,
        "total_income": total_income,
        "average_expense": average_expense,
        "highest_expense": highest_expense,
        "lowest_expense": lowest_expense,
        "category_totals": dict(category_totals),
        "top_k": top_k,
    }
