"""Tests for Flask API routes."""

import pytest
from app import create_app, db
from app.operations import create_user


@pytest.fixture
def app():
    """Create a test Flask application with an in-memory database."""
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for making HTTP requests."""
    return app.test_client()


class TestGetUsers:
    """Tests for GET /users endpoint."""

    def test_get_users_returns_200(self, client, app):
        """GET /users should return a 200 status code."""
        response = client.get('/users')
        assert response.status_code == 200

    def test_get_users_returns_json(self, client, app):
        """GET /users should return JSON content type."""
        response = client.get('/users')
        assert response.content_type == 'application/json'

    def test_get_users_empty_database(self, client, app):
        """GET /users should return an empty list when no users exist."""
        response = client.get('/users')
        data = response.get_json()
        assert data == []

    def test_get_users_returns_all_users(self, client, app):
        """GET /users should return all users with their names and balances."""
        with app.app_context():
            create_user("Alice")
            create_user("Bob")

        response = client.get('/users')
        data = response.get_json()

        assert len(data) == 2
        names = [user['name'] for user in data]
        assert 'Alice' in names
        assert 'Bob' in names

    def test_get_users_includes_balances(self, client, app):
        """Each user in the response should have an id, name, and balance."""
        with app.app_context():
            create_user("Alice")

        response = client.get('/users')
        data = response.get_json()

        assert len(data) == 1
        user = data[0]
        assert 'id' in user
        assert user['name'] == 'Alice'
        assert user['balance'] == 1000
