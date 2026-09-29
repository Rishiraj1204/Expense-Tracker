import pytest

from expense_tracker.app import create_app
from expense_tracker.models import Budget, Category, db


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


def test_budget_page(client):
    seed_user(client)
    with client.session_transaction() as session:
        user_id = session['user_id']
    with client.application.app_context():
        category = Category(user_id=user_id, name='Food', type='Expense')
        db.session.add(category)
        db.session.commit()
        category_id = category.id

    response = client.post('/budget', data={
        'category_id': str(category_id),
        'amount': '2000',
        'month': '9',
        'year': '2026'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert Budget.query.filter_by(user_id=user_id, category_id=category.id).count() == 1
