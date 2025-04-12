from flask import request, jsonify, Blueprint    # Import the necessary libraries
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity   # Import the JWTManager
from .models import db, User, bcrypt, Post                # Import the User model
from .utils import save_media_file, allowed_file


auth_bp = Blueprint('auth', __name__)    # Create a Blueprint object

@auth_bp.route('/register', methods=['POST'])    # Create a route for the register endpoint
def register():
    data = request.get_json()    # Get the data from the request
    email = data.get('email')    # Get the email from the data
    password = data.get('password')    # Get the password from the data
    
    if User.query.filter_by(email=email).first():    # Check if the email already exists
        return jsonify({'message': 'Email already exists'}), 400    # Return an error message
    
    user = User(email=email, password=password)    # Create a new user
    db.session.add(user)    # Add the user to the database
    db.session.commit()    # Commit the changes
    
    return jsonify({'message': 'User registered successfully'}), 201    # Return a success message

@auth_bp.route('/login', methods=['POST'])    # Create a route for the login endpoint
def login():
    data = request.get_json()    # Get the data from the request
    email = data.get('email')    # Get the email from the data
    password = data.get('password')    # Get the password from the data
    
    user = User.query.filter_by(email=email).first()    # Get the user from the database
    
    if not user:
        # Check if the user exists
        return jsonify({'message': 'Invalid credentials'}), 401

    if not bcrypt.check_password_hash(user.password, password):
        # Check if the password is correct
        return jsonify({'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)    # Create an access token
    return jsonify({'access_token': access_token}), 200    # Return the access token


@auth_bp.route('/post', methods=['POST'])
@jwt_required()
def create_post():
    current_user = get_jwt_identity()
    data = request.form  # Change to 'request.form' for multipart form data

    subject = data.get('subject')
    if not subject or not isinstance(subject, str):
        return jsonify({'message': 'Subject must be a string'}), 400

    content = data.get('content')
    if not content or not isinstance(content, str):
        return jsonify({'message': 'Content must be a string'}), 400

    media_url = None
    media_file = request.files.get('media_file')

    if media_file and allowed_file(media_file.filename):
        media_url = save_media_file(media_file, 'uploads')

    post = Post(user_id=current_user, subject=subject, content=content, media_url=media_url)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'}), 201


    
    
@auth_bp.route('/posts', methods=['GET'])    # Create a route for the posts endpoint
@jwt_required()    # Add a JWT required decorator
def get_posts():
    posts = Post.query.all()    # Get all the posts
    post_data = [{'id': post.id, 'content': post.content, 'media_url': post.media_url, 'created_at': post.created_at} for post in posts]    # Create a list of post data
    return jsonify(post_data), 200    # Return the post data


@auth_bp.route('/post/<int:id>', methods=['GET'])    # Create a route for the post endpoint
@jwt_required()    # Add a JWT required decorator
def get_post(id):
    post = Post.query.get(id)    # Get the post by id
    
    if not post:
        return jsonify({'message': 'Post not found'}), 404    # Return an error message
    
    post_data = {
        'id': post.id,
        'content': post.content,
        'media_url': post.media_url,
        'created_at': post.created_at
    }
    return jsonify(post_data), 200    # Return the post data

@auth_bp.route('/post/<int:id>', methods=['PUT'])    # Create a route for the update post endpoint
@jwt_required()    # Add a JWT required decorator
def update_post(id):
    current_user = get_jwt_identity()    # Get the current user
    data = request.get_json()    # Get the data from the request
    
    post = Post.query.get_or_404(id)    # Get the post by id
    
    if post.user_id != current_user:
        return jsonify({'message': 'You cannot update this post'}), 403    # Return an error message
    
    post.content = data.get('content', post.content)    # Update the content
    post.media_url = data.get('media_url', post.media_url)    # Update the media_url
    
    db.session.commit()    # Commit the changes
    
    return jsonify({
        'id': post.id,
        'content': post.content,
        'media_url': post.media_url,
        'created_at': post.created_at
    }), 200    # Return the updated post data


@auth_bp.route('/post/<int:id>', methods=['DELETE'])    # Create a route for the delete post endpoint
@jwt_required()    # Add a JWT required decorator
def delete_post(id):
    current_user = get_jwt_identity()    # Get the current user
    
    post = Post.query.get_or_404(id)    # Get the post by id
    
    if post.user_id != current_user:
        return jsonify({'message': 'You cannot delete this post'}), 403    # Return an error message
    
    db.session.delete(post)    # Delete the post
    db.session.commit()    # Commit the changes
    
    return jsonify({'message': 'Post deleted successfully'}), 200    # Return a success message

