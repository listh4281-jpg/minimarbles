"""Database operations for Minimarbles."""

from app import db
from app.models import User, BinaryTrade, UnderlyingTrade


def create_user(name):
    """
    Create a new user with the default starting balance.

    Args:
        name: The user's display name

    Returns:
        The created User object (with id populated)
    """
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return user


def create_binary_trade(party_a_id, party_b_id, stake_a, stake_b, description):
    """
    Create a new binary trade with open status.

    A binary trade is a yes/no bet between two users with potentially
    asymmetric stakes.

    Args:
        party_a_id: User ID of party A (wins if outcome is YES)
        party_b_id: User ID of party B (wins if outcome is NO)
        stake_a: Amount party A risks
        stake_b: Amount party B risks
        description: Description of the bet

    Returns:
        The created BinaryTrade object (with id populated)
    """
    trade = BinaryTrade(
        party_a_id=party_a_id,
        party_b_id=party_b_id,
        stake_a=stake_a,
        stake_b=stake_b,
        description=description,
        status="open",
        outcome=None
    )
    db.session.add(trade)
    db.session.commit()
    return trade


def create_underlying_trade(long_party_id, short_party_id, lot_size, trade_price, description):
    """
    Create a new underlying trade with open status.

    An underlying trade gives linear exposure to a price movement.
    Long party profits when price goes up, short party profits when it goes down.

    Args:
        long_party_id: User ID of the long party (profits if price rises)
        short_party_id: User ID of the short party (profits if price falls)
        lot_size: Number of units traded (can be fractional)
        trade_price: Price at which the trade is entered
        description: Description of what the trade is based on

    Returns:
        The created UnderlyingTrade object (with id populated)
    """
    trade = UnderlyingTrade(
        long_party_id=long_party_id,
        short_party_id=short_party_id,
        lot_size=lot_size,
        trade_price=trade_price,
        description=description,
        status="open",
        settlement_price=None
    )
    db.session.add(trade)
    db.session.commit()
    return trade
