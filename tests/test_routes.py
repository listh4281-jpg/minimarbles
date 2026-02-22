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


class TestPostUsers:
    """Tests for POST /users endpoint."""

    def test_create_user_returns_201(self, client, app):
        """POST /users should return 201 Created on success."""
        response = client.post('/users', json={'name': 'Alice'})
        assert response.status_code == 201

    def test_create_user_returns_user_data(self, client, app):
        """POST /users should return the created user with id, name, and balance."""
        response = client.post('/users', json={'name': 'Alice'})
        data = response.get_json()

        assert 'id' in data
        assert data['name'] == 'Alice'
        assert data['balance'] == 1000

    def test_create_user_persists(self, client, app):
        """A user created via POST /users should appear in GET /users."""
        client.post('/users', json={'name': 'Charlie'})

        response = client.get('/users')
        data = response.get_json()

        assert len(data) == 1
        assert data[0]['name'] == 'Charlie'

    def test_create_user_missing_name_returns_400(self, client, app):
        """POST /users without a name should return 400 Bad Request."""
        response = client.post('/users', json={})
        assert response.status_code == 400
