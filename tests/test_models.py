"""Tests for database models."""

import pytest
from app import create_app, db
from app.models import User, BinaryTrade


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


class TestBinaryTradeModel:
    """Tests for the BinaryTrade model."""

    def test_binary_trade_has_required_fields(self, app):
        """BinaryTrade model should have all required fields."""
        with app.app_context():
            # Create two users to be parties in the trade
            alice = User(name='Alice')
            bob = User(name='Bob')
            db.session.add_all([alice, bob])
            db.session.commit()

            # Create a binary trade
            trade = BinaryTrade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=20,
                stake_b=10,
                description='Will it rain tomorrow?'
            )
            db.session.add(trade)
            db.session.commit()

            # Verify all fields
            assert trade.id is not None
            assert trade.party_a_id == alice.id
            assert trade.party_b_id == bob.id
            assert trade.stake_a == 20
            assert trade.stake_b == 10
            assert trade.description == 'Will it rain tomorrow?'

    def test_binary_trade_default_status_is_open(self, app):
        """New binary trades should have status 'open' by default."""
        with app.app_context():
            alice = User(name='Alice')
            bob = User(name='Bob')
            db.session.add_all([alice, bob])
            db.session.commit()

            trade = BinaryTrade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=20,
                stake_b=10,
                description='Test trade'
            )
            db.session.add(trade)
            db.session.commit()

            assert trade.status == 'open'

    def test_binary_trade_outcome_is_nullable(self, app):
        """Binary trade outcome should be None until settled."""
        with app.app_context():
            alice = User(name='Alice')
            bob = User(name='Bob')
            db.session.add_all([alice, bob])
            db.session.commit()

            trade = BinaryTrade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=20,
                stake_b=10,
                description='Test trade'
            )
            db.session.add(trade)
            db.session.commit()

            # Outcome should be None for an open trade
            assert trade.outcome is None

    def test_binary_trade_can_have_outcome_set(self, app):
        """Binary trade outcome can be set to True or False."""
        with app.app_context():
            alice = User(name='Alice')
            bob = User(name='Bob')
            db.session.add_all([alice, bob])
            db.session.commit()

            trade = BinaryTrade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=20,
                stake_b=10,
                description='Test trade',
                outcome=True,
                status='settled'
            )
            db.session.add(trade)
            db.session.commit()

            assert trade.outcome is True
            assert trade.status == 'settled'

    def test_binary_trade_has_relationships_to_users(self, app):
        """BinaryTrade should have relationship accessors to party_a and party_b users."""
        with app.app_context():
            alice = User(name='Alice')
            bob = User(name='Bob')
            db.session.add_all([alice, bob])
            db.session.commit()

            trade = BinaryTrade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=20,
                stake_b=10,
                description='Test trade'
            )
            db.session.add(trade)
            db.session.commit()

            # Should be able to access the User objects through relationships
            assert trade.party_a.name == 'Alice'
            assert trade.party_b.name == 'Bob'
