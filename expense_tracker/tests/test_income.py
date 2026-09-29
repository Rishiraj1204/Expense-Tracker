import pytest

from expense_tracker.app import create_app
from expense_tracker.models import Income, User, db


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


def test_add_income(client):
    seed_user(client)
    with client.session_transaction() as session:
        user_id = session['user_id']

    response = client.post('/income/add', data={
        'source': 'Salary',
        'amount': '5000',
        'description': 'Monthly salary',
        'income_date': '2026-09-15'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert Income.query.filter_by(user_id=user_id).count() == 1
