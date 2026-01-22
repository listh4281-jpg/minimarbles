from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy database instance
db = SQLAlchemy()


def create_app():
    """Factory function that creates and configures the Flask app."""
    app = Flask(__name__)

    # Database configuration
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///minimarbles.db')

    # Initialize extensions
    db.init_app(app)

    # Import and register routes
    from app import routes
    app.register_blueprint(routes.bp)

    return app
