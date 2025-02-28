from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check required fields
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
        
    # Create user
    user = User(username=data['username'], email=data['email'])
    user.password = data['password']
    
    db.session.add(user)
    db.session.commit()
    
    # Create token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({"message": "User created", "access_token": access_token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Check required fields
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    # Check password
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Create token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({"access_token": access_token}), 200