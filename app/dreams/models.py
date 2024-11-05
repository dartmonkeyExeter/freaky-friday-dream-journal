from datetime import datetime
from app.extensions import db

class Dream(db.Model):
    __tablename__ = 'dreams'
    
    dream_id = db.Column(db.String, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.String, db.ForeignKey('users.user_id'), nullable=False)
    tag = db.Column(db.String)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    private = db.Column(db.Boolean, default=False)
