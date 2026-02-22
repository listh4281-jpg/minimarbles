from flask import Blueprint, jsonify, request
from app.operations import list_all_users, create_user

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


@bp.route('/users', methods=['POST'])
def post_user():
    """Create a new user from JSON body with a 'name' field."""
    data = request.get_json()
    name = data.get('name') if data else None
    if not name:
        return jsonify({'error': 'name is required'}), 400

    user = create_user(name)
    return jsonify({'id': user.id, 'name': user.name, 'balance': user.balance}), 201
