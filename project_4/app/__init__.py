from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, IMAGES, configure_uploads
from .models import db, bcrypt
from .routes import auth_bp
import os

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['JWT_SECRET_KEY'] = "Mohadek"
    
    # File upload configurations
    photos = UploadSet('photos', IMAGES)
    app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
    configure_uploads(app, photos)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')

    
    # Create all database tables
    with app.app_context():
        db.create_all()
    
    return app
