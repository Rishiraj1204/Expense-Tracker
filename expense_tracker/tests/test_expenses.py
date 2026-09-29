from datetime import date

import pytest

from expense_tracker.app import create_app
from expense_tracker.models import Category, Expense, db


@pytest.fixture
def app():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite://')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def seed_user(client):
    client.post('/register', data={
        'name': 'Alice',
        'email': 'alice@example.com',
        'password': 'secret123',
        'confirm_password': 'secret123'
    })
    client.post('/login', data={
        'email': 'alice@example.com',
        'password': 'secret123'
    })


def test_add_expense(client):
    seed_user(client)
    with client.session_transaction() as session:
        user_id = session['user_id']
    with client.application.app_context():
        category = Category(user_id=user_id, name='Food', type='Expense')
        db.session.add(category)
        db.session.commit()
        category_id = category.id

    response = client.post('/expenses/add', data={
        'amount': '250',
        'category_id': str(category_id),
        'description': 'Groceries',
        'payment_method': 'UPI',
        'expense_date': '2026-09-10'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert Expense.query.count() == 1


def test_update_and_delete_expense(client):
    seed_user(client)
    with client.session_transaction() as session:
        user_id = session['user_id']
    with client.application.app_context():
        category = Category(user_id=user_id, name='Food', type='Expense')
        db.session.add(category)
        db.session.commit()
        category_id = category.id
        expense = Expense(user_id=user_id, category_id=category_id, amount=100, description='Lunch', payment_method='Cash', expense_date=date(2026, 9, 1))
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    response = client.post(f'/expenses/edit/{expense_id}', data={
        'amount': '150',
        'category_id': str(category_id),
        'description': 'Lunch update',
        'payment_method': 'UPI',
        'expense_date': '2026-09-02'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert Expense.query.get(expense_id).description == 'Lunch update'

    response = client.get(f'/expenses/delete/{expense_id}', follow_redirects=True)
    assert response.status_code == 200
    assert Expense.query.count() == 0
