"""Tests for pure business logic functions."""

from app.logic import calculate_binary_payout


class TestBinaryPayout:
    """Tests for binary trade payout calculation."""

    def test_outcome_yes_alice_wins(self):
        """When outcome is YES, Alice wins Bob's stake."""
        alice_stake = 20
        bob_stake = 10
        outcome = True  # YES

        alice_pnl, bob_pnl = calculate_binary_payout(alice_stake, bob_stake, outcome)

        # Alice wins Bob's stake
        assert alice_pnl == 10
        # Bob loses his stake
        assert bob_pnl == -10

    def test_outcome_no_bob_wins(self):
        """When outcome is NO, Bob wins Alice's stake."""
        alice_stake = 20
        bob_stake = 10
        outcome = False  # NO

        alice_pnl, bob_pnl = calculate_binary_payout(alice_stake, bob_stake, outcome)

        # Alice loses her stake
        assert alice_pnl == -20
        # Bob wins Alice's stake
        assert bob_pnl == 20

    def test_payout_is_zero_sum_yes(self):
        """Total P&L should be zero (minimarbles are conserved)."""
        alice_pnl, bob_pnl = calculate_binary_payout(50, 25, True)
        assert alice_pnl + bob_pnl == 0

    def test_payout_is_zero_sum_no(self):
        """Total P&L should be zero (minimarbles are conserved)."""
        alice_pnl, bob_pnl = calculate_binary_payout(50, 25, False)
        assert alice_pnl + bob_pnl == 0

    def test_equal_stakes(self):
        """Works correctly when both parties stake the same amount."""
        alice_pnl, bob_pnl = calculate_binary_payout(100, 100, True)
        assert alice_pnl == 100
        assert bob_pnl == -100
