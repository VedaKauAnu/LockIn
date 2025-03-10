import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.extensions import db, migrate, jwt

def create_app():
    app = Flask(__name__)
    
    # Config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enable CORS
    CORS(app)
    
    # Basic routes to verify API is working
    @app.route('/')
    def index():
        return jsonify({'message': 'Server is running'})

    @app.route('/api/test')
    def test():
        return jsonify({'message': 'API is working!'})
    
    # Register blueprints
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from app.api.courses import courses_bp
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    
    from app.api.notes import notes_bp
    app.register_blueprint(notes_bp, url_prefix='/api')
    
    from app.api.questions import questions_bp
    app.register_blueprint(questions_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app