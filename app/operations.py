"""Database operations for Minimarbles."""

from app import db
from app.models import User, BinaryTrade, UnderlyingTrade
from app.logic import calculate_binary_payout, calculate_underlying_payout


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


def settle_binary_trade(trade_id, outcome):
    """
    Settle a binary trade and update both users' balances.

    Args:
        trade_id: The ID of the trade to settle
        outcome: True for YES (party A wins), False for NO (party B wins)

    Returns:
        The updated BinaryTrade object
    """
    trade = db.session.get(BinaryTrade, trade_id)

    # Calculate P&L using the pure business logic function
    party_a_pnl, party_b_pnl = calculate_binary_payout(
        trade.stake_a, trade.stake_b, outcome
    )

    # Update user balances
    trade.party_a.balance += party_a_pnl
    trade.party_b.balance += party_b_pnl

    # Update trade status
    trade.outcome = outcome
    trade.status = "settled"

    db.session.commit()
    return trade


def settle_underlying_trade(trade_id, settlement_price):
    """
    Settle an underlying trade and update both users' balances.

    Args:
        trade_id: The ID of the trade to settle
        settlement_price: The final price to settle the trade at

    Returns:
        The updated UnderlyingTrade object
    """
    trade = db.session.get(UnderlyingTrade, trade_id)

    # Calculate P&L using the pure business logic function
    long_pnl, short_pnl = calculate_underlying_payout(
        trade.lot_size, trade.trade_price, settlement_price
    )

    # Update user balances
    trade.long_party.balance += long_pnl
    trade.short_party.balance += short_pnl

    # Update trade status
    trade.settlement_price = settlement_price
    trade.status = "settled"

    db.session.commit()
    return trade
