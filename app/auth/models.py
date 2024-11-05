from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
