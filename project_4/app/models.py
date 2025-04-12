from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Add a foreign key to the user table
    content = db.Column(db.String(280), nullable=False)  # Add a content column
    media_url = db.Column(db.String(120), nullable=True)  # Add a media_url column
    subject = db.Column(db.String(100), nullable=True)  # Add a subject column (new field)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Add a created_at column
    
    user = db.relationship('User', backref='posts', lazy=True)  # Add a relationship to the user table
    
    def __repr__(self):
        return f"<Post '{self.id} {self.content}'>"
