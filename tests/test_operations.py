"""Tests for database operations."""

import pytest
from app import create_app, db
from app.models import User, BinaryTrade, UnderlyingTrade
from app.operations import create_user, create_binary_trade, create_underlying_trade, settle_binary_trade, settle_underlying_trade


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


class TestCreateBinaryTrade:
    """Tests for binary trade creation."""

    def test_create_binary_trade_basic(self, app):
        """Should create a binary trade with open status."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_binary_trade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=20,
                stake_b=10,
                description="Will it rain tomorrow?"
            )

            assert trade.id is not None
            assert trade.party_a_id == alice.id
            assert trade.party_b_id == bob.id
            assert trade.stake_a == 20
            assert trade.stake_b == 10
            assert trade.description == "Will it rain tomorrow?"
            assert trade.status == "open"
            assert trade.outcome is None

    def test_create_binary_trade_persists(self, app):
        """Created trade should be retrievable from the database."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_binary_trade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=50,
                stake_b=25,
                description="Will the coin flip be heads?"
            )
            trade_id = trade.id

            # Query the database directly to verify persistence
            found_trade = db.session.get(BinaryTrade, trade_id)

            assert found_trade is not None
            assert found_trade.description == "Will the coin flip be heads?"
            assert found_trade.status == "open"

    def test_create_binary_trade_relationships(self, app):
        """Trade should have proper relationships to users."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_binary_trade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=30,
                stake_b=15,
                description="Test trade"
            )

            # Verify relationships work
            assert trade.party_a.name == "Alice"
            assert trade.party_b.name == "Bob"


class TestCreateUnderlyingTrade:
    """Tests for underlying trade creation."""

    def test_create_underlying_trade_basic(self, app):
        """Should create an underlying trade with open status."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_underlying_trade(
                long_party_id=alice.id,
                short_party_id=bob.id,
                lot_size=10,
                trade_price=100.0,
                description="AAPL stock price at end of month"
            )

            assert trade.id is not None
            assert trade.long_party_id == alice.id
            assert trade.short_party_id == bob.id
            assert trade.lot_size == 10
            assert trade.trade_price == 100.0
            assert trade.description == "AAPL stock price at end of month"
            assert trade.status == "open"
            assert trade.settlement_price is None

    def test_create_underlying_trade_persists(self, app):
        """Created trade should be retrievable from the database."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_underlying_trade(
                long_party_id=alice.id,
                short_party_id=bob.id,
                lot_size=5.5,
                trade_price=50.0,
                description="Gold price prediction"
            )
            trade_id = trade.id

            # Query the database directly to verify persistence
            found_trade = db.session.get(UnderlyingTrade, trade_id)

            assert found_trade is not None
            assert found_trade.description == "Gold price prediction"
            assert found_trade.lot_size == 5.5
            assert found_trade.status == "open"

    def test_create_underlying_trade_relationships(self, app):
        """Trade should have proper relationships to users."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_underlying_trade(
                long_party_id=alice.id,
                short_party_id=bob.id,
                lot_size=1,
                trade_price=200.0,
                description="Test underlying trade"
            )

            # Verify relationships work
            assert trade.long_party.name == "Alice"
            assert trade.short_party.name == "Bob"


class TestSettleBinaryTrade:
    """Tests for settling binary trades."""

    def test_settle_binary_trade_yes_outcome(self, app):
        """Settling with YES should transfer stake_b from Bob to Alice."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_binary_trade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=20,
                stake_b=10,
                description="Will it rain?"
            )

            # Settle with YES outcome - Alice wins
            settled_trade = settle_binary_trade(trade.id, outcome=True)

            # Trade should be updated
            assert settled_trade.status == "settled"
            assert settled_trade.outcome is True

            # Refresh users from database to get updated balances
            alice = db.session.get(User, alice.id)
            bob = db.session.get(User, bob.id)

            # Alice wins Bob's stake (10), Bob loses his stake (10)
            assert alice.balance == 1010  # 1000 + 10
            assert bob.balance == 990     # 1000 - 10

    def test_settle_binary_trade_no_outcome(self, app):
        """Settling with NO should transfer stake_a from Alice to Bob."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_binary_trade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=20,
                stake_b=10,
                description="Will it rain?"
            )

            # Settle with NO outcome - Bob wins
            settled_trade = settle_binary_trade(trade.id, outcome=False)

            # Trade should be updated
            assert settled_trade.status == "settled"
            assert settled_trade.outcome is False

            # Refresh users from database to get updated balances
            alice = db.session.get(User, alice.id)
            bob = db.session.get(User, bob.id)

            # Bob wins Alice's stake (20), Alice loses her stake (20)
            assert alice.balance == 980   # 1000 - 20
            assert bob.balance == 1020    # 1000 + 20

    def test_settle_binary_trade_zero_sum(self, app):
        """Total minimarbles should be conserved after settlement."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_binary_trade(
                party_a_id=alice.id,
                party_b_id=bob.id,
                stake_a=50,
                stake_b=25,
                description="Test trade"
            )

            total_before = alice.balance + bob.balance

            settle_binary_trade(trade.id, outcome=True)

            # Refresh users
            alice = db.session.get(User, alice.id)
            bob = db.session.get(User, bob.id)

            total_after = alice.balance + bob.balance

            # Minimarbles are conserved
            assert total_before == total_after


class TestSettleUnderlyingTrade:
    """Tests for settling underlying trades."""

    def test_settle_underlying_trade_price_goes_up(self, app):
        """Settling when price rises should transfer minimarbles to long party."""
        with app.app_context():
            alice = create_user("Alice")  # long party
            bob = create_user("Bob")      # short party

            trade = create_underlying_trade(
                long_party_id=alice.id,
                short_party_id=bob.id,
                lot_size=10,
                trade_price=100.0,
                description="AAPL price prediction"
            )

            # Settle with price going up: 110 > 100
            settled_trade = settle_underlying_trade(trade.id, settlement_price=110.0)

            # Trade should be updated
            assert settled_trade.status == "settled"
            assert settled_trade.settlement_price == 110.0

            # Refresh users from database to get updated balances
            alice = db.session.get(User, alice.id)
            bob = db.session.get(User, bob.id)

            # P&L = lot_size * (settlement - trade) = 10 * (110 - 100) = 100
            # Long wins 100, short loses 100
            assert alice.balance == 1100  # 1000 + 100
            assert bob.balance == 900     # 1000 - 100

    def test_settle_underlying_trade_price_goes_down(self, app):
        """Settling when price falls should transfer minimarbles to short party."""
        with app.app_context():
            alice = create_user("Alice")  # long party
            bob = create_user("Bob")      # short party

            trade = create_underlying_trade(
                long_party_id=alice.id,
                short_party_id=bob.id,
                lot_size=10,
                trade_price=100.0,
                description="AAPL price prediction"
            )

            # Settle with price going down: 80 < 100
            settled_trade = settle_underlying_trade(trade.id, settlement_price=80.0)

            # Trade should be updated
            assert settled_trade.status == "settled"
            assert settled_trade.settlement_price == 80.0

            # Refresh users from database to get updated balances
            alice = db.session.get(User, alice.id)
            bob = db.session.get(User, bob.id)

            # P&L = lot_size * (settlement - trade) = 10 * (80 - 100) = -200
            # Long loses 200, short wins 200
            assert alice.balance == 800   # 1000 - 200
            assert bob.balance == 1200    # 1000 + 200

    def test_settle_underlying_trade_zero_sum(self, app):
        """Total minimarbles should be conserved after settlement."""
        with app.app_context():
            alice = create_user("Alice")
            bob = create_user("Bob")

            trade = create_underlying_trade(
                long_party_id=alice.id,
                short_party_id=bob.id,
                lot_size=5.5,
                trade_price=50.0,
                description="Test trade"
            )

            total_before = alice.balance + bob.balance

            settle_underlying_trade(trade.id, settlement_price=75.0)

            # Refresh users
            alice = db.session.get(User, alice.id)
            bob = db.session.get(User, bob.id)

            total_after = alice.balance + bob.balance

            # Minimarbles are conserved
            assert total_before == total_after
