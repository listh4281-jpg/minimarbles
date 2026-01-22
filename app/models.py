"""Database models for Minimarbles."""

from app import db


class User(db.Model):
    """A user who can trade minimarbles."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer, default=1000)


class BinaryTrade(db.Model):
    """A binary (yes/no) trade between two users."""

    id = db.Column(db.Integer, primary_key=True)
    party_a_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    party_b_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stake_a = db.Column(db.Integer, nullable=False)
    stake_b = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    outcome = db.Column(db.Boolean, nullable=True)  # None=open, True/False=settled
    status = db.Column(db.String(20), default='open')

    # Relationships to access User objects directly
    party_a = db.relationship('User', foreign_keys=[party_a_id])
    party_b = db.relationship('User', foreign_keys=[party_b_id])
