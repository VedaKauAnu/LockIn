from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course, Note

courses_bp = Blueprint('courses', __name__)

# Get all courses for current user
@courses_bp.route('/', methods=['GET'])
@jwt_required()
def get_courses():
    current_user_id = get_jwt_identity()
    courses = Course.query.filter_by(user_id=current_user_id).all()
    
    result = []
    for course in courses:
        result.append({
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'created_at': course.created_at.isoformat()
        })
    
    return jsonify(result), 200

# Create a new course
@courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400
    
    new_course = Course(
        title=data['title'],
        description=data.get('description', ''),
        user_id=current_user_id
    )
    
    db.session.add(new_course)
    db.session.commit()
    
    return jsonify({
        'id': new_course.id,
        'title': new_course.title,
        'description': new_course.description,
        'created_at': new_course.created_at.isoformat()
    }), 201

# Get a specific course
@courses_bp.route('/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    current_user_id = get_jwt_identity()
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    return jsonify({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'created_at': course.created_at.isoformat()
    }), 200

# Update a course
@courses_bp.route('/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    current_user_id = get_jwt_identity()
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        course.title = data['title']
    if 'description' in data:
        course.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'created_at': course.created_at.isoformat()
    }), 200

# Delete a course
@courses_bp.route('/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    current_user_id = get_jwt_identity()
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({"message": "Course deleted successfully"}), 200