from flask import Flask, request, jsonify, session
from flask_cors import CORS

from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os

from model import db, user, Post

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)    # Ensure folder exists

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if data is None:
        return jsonify({'message': 'No data provided'}), 400
    
    if user.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400
    
    users = user(username=username, password=password)
    db.session.add(users)
    db.session.commit()
    
    return jsonify({'message': 'User created'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if data is None:
        return jsonify({'message': 'No data provided'}), 400
    
    uzer =  user.query.filter_by(username=username, password=password).first()
    if uzer:
        session['user_id'] = uzer.id
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({"message": "Invalid username or password"}), 401
    
@app.route('/upload', methods=['POST'])
def create_post():
    if "user_id" not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    title = request.form.get('title')
    description = request.form.get('description')
    image = request.files.get('image')
    
    if not title or not description or not image or not user_id:
        return jsonify({'message': 'Missing data'}), 400
    
    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)
    
    new_post = Post(
        title=title,
        description=description,
        image_path=image_path,
        user_id=user_id
    )
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({'message': 'Post created'}), 201


@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'image_path': post.image_path,
            'created_at': post.created_at
        })
    return jsonify(data), 200

@app.route('/posts/<int:id>', methods=['PUT'])
def post_update(post_id):
    if "uzer_id" not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    
    if post.user_id != session['user_id']:
        return jsonify({'message': 'Unauthorized'}), 401
    
    title = request.form.get('title')
    description = request.form.get('description')
    image = request.files.get('image')
    
    if title:
        post.title = title
    if description:
        post.description = description
    if image:
        if os.path.exists(post.image_path):
            os.remove(post.image_path)
            
        filename = secure_filename(image.filename)  
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        post.image_path = image_path
    
    db.session.commit()
    
    return jsonify({'message': 'Post updated'}), 200

@app.route('/posts/<int:id>', methods=['DELETE'])
def del_post(post_id):
    if "user_id" not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    
    if post.user_id != session['user_id']:
        return jsonify({'message': 'Unauthorized'}), 401
    
    if os.path.exists(post.image_path):
        os.remove(post.image_path)
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted'}), 200
    
    
if __name__ == '__main__':
    app.run(debug=True)