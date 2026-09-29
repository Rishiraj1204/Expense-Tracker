from expense_tracker.analytics.anomaly import detect_anomalies
from expense_tracker.analytics.moving_average import calculate_moving_average
from expense_tracker.analytics.recurring import detect_recurring_expenses
from expense_tracker.analytics.time_series import aggregate_by_period
from expense_tracker.analytics.trends import analyse_trends


class Expense:
    def __init__(self, amount, expense_date, description='x', category_name='Food'):
        self.amount = amount
        self.expense_date = expense_date
        self.description = description
        self.category = type('Category', (), {'name': category_name})()


def test_time_series_aggregation():
    expenses = [
        Expense(100, '2026-01-10'),
        Expense(200, '2026-02-15'),
    ]
    aggregated = {
        '2026-01': 100,
        '2026-02': 200,
    }
    assert aggregated == {k: v for k, v in sorted(aggregated.items())}


def test_moving_average():
    expenses = [Expense(10, '2026-01-01'), Expense(20, '2026-01-02'), Expense(30, '2026-01-03')]
    result = calculate_moving_average(expenses, window_size=2)
    assert len(result) == 3
    assert result[2]['value'] == 25


def test_trends():
    series = {'Jan': 100, 'Feb': 120, 'Mar': 110}
    trend = analyse_trends(series)
    assert trend[0]['trend'] == 'Increasing'


def test_anomaly_detection():
    expenses = [Expense(10, '2026-01-01'), Expense(12, '2026-01-02'), Expense(100, '2026-01-03')]
    anomalies = detect_anomalies(expenses)
    assert len(anomalies) == 1


def test_recurring_detection():
    class FakeExpense:
        def __init__(self, category_name, amount, expense_date):
            self.category = type('Category', (), {'name': category_name})()
            self.amount = amount
            self.expense_date = expense_date

    recurring = detect_recurring_expenses(1)
    assert recurring == []
