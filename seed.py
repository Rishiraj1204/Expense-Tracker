from datetime import date

from expense_tracker.app import create_app
from expense_tracker.models import Budget, Category, Expense, Income, Notification, User, db
from werkzeug.security import generate_password_hash


app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(name='Demo User', email='demo@example.com', password_hash=generate_password_hash('demo123'))
    db.session.add(user)
    db.session.commit()

    categories = [
        Category(user_id=user.id, name='Food', type='Expense'),
        Category(user_id=user.id, name='Travel', type='Expense'),
        Category(user_id=user.id, name='Bills', type='Expense'),
        Category(user_id=user.id, name='Salary', type='Income'),
    ]
    db.session.add_all(categories)
    db.session.commit()

    db.session.add_all([
        Income(user_id=user.id, source='Salary', amount=35000, description='Monthly salary', income_date=date(2026, 9, 1)),
        Expense(user_id=user.id, category_id=categories[0].id, amount=2500, description='Groceries', payment_method='UPI', expense_date=date(2026, 9, 2)),
        Expense(user_id=user.id, category_id=categories[1].id, amount=4200, description='Travel tickets', payment_method='Credit Card', expense_date=date(2026, 9, 5)),
        Expense(user_id=user.id, category_id=categories[2].id, amount=6500, description='Electricity bill', payment_method='Bank Transfer', expense_date=date(2026, 9, 8)),
    ])
    db.session.commit()

    db.session.add_all([
        Budget(user_id=user.id, category_id=None, amount=20000, month=9, year=2026),
        Budget(user_id=user.id, category_id=categories[0].id, amount=5000, month=9, year=2026),
        Notification(user_id=user.id, title='Budget Alert', message='Food budget reached 75%.', type='warning', is_read=False),
    ])
    db.session.commit()

    print('Seed data created successfully.')
