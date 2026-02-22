from flask import Blueprint, jsonify
from app.operations import list_all_users

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page - just a hello world for now."""
    return 'Hello, Minimarbles!'


@bp.route('/users')
def get_users():
    """Return all users and their balances as JSON."""
    users = list_all_users()
    return jsonify([
        {'id': user.id, 'name': user.name, 'balance': user.balance}
        for user in users
    ])
