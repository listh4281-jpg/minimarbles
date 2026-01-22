"""Tests for database operations."""

import pytest
from app import create_app, db
from app.models import User
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
    """Create a test client."""
    return app.test_client()


class TestCreateUser:
    """Tests for user creation."""

    def test_create_user_with_default_balance(self, app):
        """New user should be created with 1000 minimarbles."""
        with app.app_context():
            user = create_user("Alice")

            assert user.name == "Alice"
            assert user.balance == 1000
            assert user.id is not None

    def test_create_user_persists_to_database(self, app):
        """Created user should be retrievable from the database."""
        with app.app_context():
            user = create_user("Bob")
            user_id = user.id

            # Query the database directly to verify persistence
            found_user = db.session.get(User, user_id)

            assert found_user is not None
            assert found_user.name == "Bob"
            assert found_user.balance == 1000

    def test_create_multiple_users(self, app):
        """Should be able to create multiple users."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            assert alice.id != bob.id
            assert User.query.count() == 2
