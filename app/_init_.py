 from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import models
    from models.user import User
    from models.passenger import Passenger
    from models.flight import Flight
    from models.baggage import Baggage
    from models.assistance import AssistanceRequest

    # Load logged-in user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register application routes
    from app.routes import main
    from app.auth import auth
    from app.passenger import passenger
    from app.staff import staff
    from app.admin import admin
    from app.api import api

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(passenger)
    app.register_blueprint(staff)
    app.register_blueprint(admin)
    app.register_blueprint(api)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app