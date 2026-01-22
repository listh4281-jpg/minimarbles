"""Pure business logic functions for trade calculations."""


def calculate_binary_payout(alice_stake, bob_stake, outcome):
    """
    Calculate P&L for a binary trade.

    A binary trade has two parties with asymmetric stakes betting on a yes/no outcome.
    - If outcome is YES (True): Alice wins Bob's stake
    - If outcome is NO (False): Bob wins Alice's stake

    Args:
        alice_stake: Amount Alice risks (she wins if outcome is YES)
        bob_stake: Amount Bob risks (he wins if outcome is NO)
        outcome: True for YES, False for NO

    Returns:
        Tuple of (alice_pnl, bob_pnl) - always zero-sum
    """
    if outcome:
        # YES: Alice wins Bob's stake
        alice_pnl = bob_stake
        bob_pnl = -bob_stake
    else:
        # NO: Bob wins Alice's stake
        alice_pnl = -alice_stake
        bob_pnl = alice_stake

    return alice_pnl, bob_pnl
