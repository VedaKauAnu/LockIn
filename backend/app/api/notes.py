from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course, Note
from app.ai_service import AIService

notes_bp = Blueprint('notes', __name__)
ai_service = AIService()

# Get all notes for a course
@notes_bp.route('/course/<int:course_id>/notes', methods=['GET'])
@jwt_required()
def get_notes(course_id):
    current_user_id = get_jwt_identity()
    
    # Verify course belongs to user
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    notes = Note.query.filter_by(course_id=course_id).all()
    
    result = []
    for note in notes:
        result.append({
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'created_at': note.created_at.isoformat(),
            'course_id': note.course_id
        })
    
    return jsonify(result), 200

# Create a new note
@notes_bp.route('/course/<int:course_id>/notes', methods=['POST'])
@jwt_required()
def create_note(course_id):
    current_user_id = get_jwt_identity()
    
    # Verify course belongs to user
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required"}), 400
    
    new_note = Note(
        title=data['title'],
        content=data['content'],
        course_id=course_id
    )
    
    db.session.add(new_note)
    db.session.commit()
    
    return jsonify({
        'id': new_note.id,
        'title': new_note.title,
        'content': new_note.content,
        'created_at': new_note.created_at.isoformat(),
        'course_id': new_note.course_id
    }), 201

# Get a specific note
@notes_bp.route('/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    current_user_id = get_jwt_identity()
    
    # Join note with course to verify ownership
    note = db.session.query(Note).join(Course).filter(
        Note.id == note_id,
        Course.user_id == current_user_id
    ).first()
    
    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat(),
        'course_id': note.course_id
    }), 200

# Update a note
@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    current_user_id = get_jwt_identity()
    
    # Join note with course to verify ownership
    note = db.session.query(Note).join(Course).filter(
        Note.id == note_id,
        Course.user_id == current_user_id
    ).first()
    
    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    
    db.session.commit()
    
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat(),
        'course_id': note.course_id
    }), 200

# Delete a note
@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    current_user_id = get_jwt_identity()
    
    # Join note with course to verify ownership
    note = db.session.query(Note).join(Course).filter(
        Note.id == note_id,
        Course.user_id == current_user_id
    ).first()
    
    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    db.session.delete(note)
    db.session.commit()
    
    return jsonify({"message": "Note deleted successfully"}), 200

# Generate notes with AI
@notes_bp.route('/course/<int:course_id>/generate-notes', methods=['POST'])
@jwt_required()
def generate_notes(course_id):
    current_user_id = get_jwt_identity()
    
    # Verify course belongs to user
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    data = request.get_json()
    if not data or not data.get('topic'):
        return jsonify({"error": "Topic is required"}), 400
    
    # Get optional detail level
    detail_level = data.get('detail_level', 'medium')
    
    try:
        # Generate notes using AI service
        generated_content = ai_service.generate_notes(
            course_title=course.title,
            topic=data['topic'],
            detail_level=detail_level
        )
        
        # Create a new note with generated content
        new_note = Note(
            title=f"Notes: {data['topic']}",
            content=generated_content,
            course_id=course_id
        )
        
        db.session.add(new_note)
        db.session.commit()
        
        return jsonify({
            'id': new_note.id,
            'title': new_note.title,
            'content': new_note.content,
            'created_at': new_note.created_at.isoformat(),
            'course_id': new_note.course_id
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500