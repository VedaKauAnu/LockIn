from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Username, email, and password are required"}), 400
    
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.password = data['password']  # This will hash the password
    
    db.session.add(new_user)
    db.session.commit()
    
    # Generate access token
    access_token = create_access_token(identity=new_user.id)
    
    return jsonify({"message": "User registered successfully", "access_token": access_token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required"}), 400
    
    # Find user by username
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid username or password"}), 401
    
    # Generate access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({"message": "Login successful", "access_token": access_token}), 200