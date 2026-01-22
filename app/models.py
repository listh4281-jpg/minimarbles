"""Database models for Minimarbles."""

from app import db


class User(db.Model):
    """A user who can trade minimarbles."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer, default=1000)
