from flask import Blueprint

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page - just a hello world for now."""
    return 'Hello, Minimarbles!'
