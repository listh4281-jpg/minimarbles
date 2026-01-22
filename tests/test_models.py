"""Tests for database models."""

import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    """Create a test Flask app with an in-memory SQLite database."""
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


class TestUserModel:
    """Tests for the User model."""

    def test_user_has_required_fields(self, app):
        """User model should have id, name, and balance fields."""
        with app.app_context():
            user = User(name='Alice')
            db.session.add(user)
            db.session.commit()

            # Verify user was saved with an auto-generated id
            assert user.id is not None
            assert user.name == 'Alice'
            # Balance should have a default value
            assert user.balance is not None

    def test_user_default_balance_is_1000(self, app):
        """New users should start with 1000 minimarbles."""
        with app.app_context():
            user = User(name='Bob')
            db.session.add(user)
            db.session.commit()

            assert user.balance == 1000

    def test_user_can_have_custom_balance(self, app):
        """Users can be created with a custom starting balance."""
        with app.app_context():
            user = User(name='Charlie', balance=500)
            db.session.add(user)
            db.session.commit()

            assert user.balance == 500

    def test_user_name_is_required(self, app):
        """User must have a name."""
        with app.app_context():
            user = User(name=None)
            db.session.add(user)

            # Should raise an error when trying to commit a user without a name
            with pytest.raises(Exception):
                db.session.commit()
