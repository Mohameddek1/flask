from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Relationship User and Post
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model):
    id  =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)