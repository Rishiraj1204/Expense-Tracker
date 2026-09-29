import pytest
from flask import session

from expense_tracker.app import create_app
from expense_tracker.models import User, db


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


def test_register_and_login(client):
    response = client.post('/register', data={
        'name': 'Alice',
        'email': 'alice@example.com',
        'password': 'secret123',
        'confirm_password': 'secret123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert User.query.filter_by(email='alice@example.com').count() == 1

    response = client.post('/login', data={
        'email': 'alice@example.com',
        'password': 'secret123'
    }, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess['user_id'] is not None


def test_duplicate_email(client):
    client.post('/register', data={
        'name': 'Alice',
        'email': 'alice@example.com',
        'password': 'secret123',
        'confirm_password': 'secret123'
    })
    response = client.post('/register', data={
        'name': 'Bob',
        'email': 'alice@example.com',
        'password': 'secret123',
        'confirm_password': 'secret123'
    }, follow_redirects=True)
    assert b'An account with this email already exists.' in response.data
