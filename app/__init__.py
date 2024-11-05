from flask import Flask
from app.extensions import db
from app.dreams.views import dreams_bp
from app.auth.views import auth_bp
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dreams_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "your_secret_key"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(dreams_bp)
    app.register_blueprint(auth_bp)

    return app
