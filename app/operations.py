"""Database operations for Minimarbles."""

from app import db
from app.models import User


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
