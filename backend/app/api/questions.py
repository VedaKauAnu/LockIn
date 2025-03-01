from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course, PracticeQuestion

questions_bp = Blueprint('questions', __name__)

# Get all practice questions for a course
@questions_bp.route('/course/<int:course_id>/questions', methods=['GET'])
@jwt_required()
def get_questions(course_id):
    current_user_id = get_jwt_identity()
    
    # Verify course belongs to user
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    questions = PracticeQuestion.query.filter_by(course_id=course_id).all()
    
    result = []
    for question in questions:
        result.append({
            'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'difficulty': question.difficulty,
            'created_at': question.created_at.isoformat(),
            'course_id': question.course_id
        })
    
    return jsonify(result), 200

# Create a new practice question
@questions_bp.route('/course/<int:course_id>/questions', methods=['POST'])
@jwt_required()
def create_question(course_id):
    current_user_id = get_jwt_identity()
    
    # Verify course belongs to user
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    data = request.get_json()
    
    if not data or not data.get('question') or not data.get('answer'):
        return jsonify({"error": "Question and answer are required"}), 400
    
    new_question = PracticeQuestion(
        question=data['question'],
        answer=data['answer'],
        difficulty=data.get('difficulty', 'medium'),
        course_id=course_id
    )
    
    db.session.add(new_question)
    db.session.commit()
    
    return jsonify({
        'id': new_question.id,
        'question': new_question.question,
        'answer': new_question.answer,
        'difficulty': new_question.difficulty,
        'created_at': new_question.created_at.isoformat(),
        'course_id': new_question.course_id
    }), 201

# Generate practice questions with AI
@questions_bp.route('/course/<int:course_id>/generate-questions', methods=['POST'])
@jwt_required()
def generate_questions(course_id):
    current_user_id = get_jwt_identity()
    
    # Verify course belongs to user
    course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    data = request.get_json()
    if not data or not data.get('topic') or not data.get('count'):
        return jsonify({"error": "Topic and count are required"}), 400
    
    try:
        count = int(data['count'])
        if count <= 0 or count > 20:
            return jsonify({"error": "Count must be between 1 and 20"}), 400
    except ValueError:
        return jsonify({"error": "Count must be a number"}), 400
    
    # TODO: Implement actual AI generation with OpenAI/LangChain
    # For now, generate placeholder questions
    
    result = []
    for i in range(count):
        question = PracticeQuestion(
            question=f"Sample question #{i+1} about {data['topic']} in {course.title}?",
            answer=f"This is the answer to question #{i+1}.",
            difficulty=["easy", "medium", "hard"][i % 3],
            course_id=course_id
        )
        
        db.session.add(question)
        
        result.append({
            'question': question.question,
            'answer': question.answer,
            'difficulty': question.difficulty
        })
    
    db.session.commit()
    
    return jsonify({
        'message': f"Generated {count} practice questions",
        'questions': result
    }), 201