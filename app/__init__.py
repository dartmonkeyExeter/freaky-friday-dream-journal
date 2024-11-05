from flask import Flask
from app.extensions import db
from app.dreams.views import dreams_bp
from app.auth.views import auth_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dreams_db.sqlite'
    app.config['SECRET_KEY'] = "your_secret_key"

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(dreams_bp, url_prefix='/dreams')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
