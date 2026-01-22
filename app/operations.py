"""Database operations for Minimarbles."""

from app import db
from app.models import User, BinaryTrade


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
