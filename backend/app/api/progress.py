from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course, PracticeQuestion
from app.models.progress_models import StudyProgress, DailyStudy, StudySession, Todo
from datetime import datetime, date, timedelta
import json

progress_bp = Blueprint('progress', __name__)

# Record question progress (confidence level)
@progress_bp.route('/question-progress', methods=['POST'])
@jwt_required()
def record_question_progress():
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    if not data or not data.get('question_id') or not data.get('confidence_level'):
        return jsonify({"error": "Question ID and confidence level are required"}), 400
    
    question_id = data.get('question_id')
    confidence_level = data.get('confidence_level')
    
    # Validate confidence level (1-3)
    if confidence_level not in [1, 2, 3]:
        return jsonify({"error": "Confidence level must be 1, 2, or 3"}), 400
    
    # Verify the question exists and user has access to it
    question = db.session.query(PracticeQuestion).join(Course).filter(
        PracticeQuestion.id == question_id,
        Course.user_id == current_user_id
    ).first()
    
    if not question:
        return jsonify({"error": "Question not found or you don't have access"}), 404
    
    # Create or update progress record
    progress = StudyProgress.query.filter_by(
        user_id=current_user_id,
        question_id=question_id
    ).first()
    
    if progress:
        progress.confidence_level = confidence_level
    else:
        progress = StudyProgress(
            user_id=current_user_id,
            course_id=question.course_id,
            question_id=question_id,
            confidence_level=confidence_level
        )
        db.session.add(progress)
    
    db.session.commit()
    
    return jsonify({
        "message": "Progress recorded successfully",
        "question_id": question_id,
        "confidence_level": confidence_level
    }), 200

# Start a new study session
@progress_bp.route('/study-session/start', methods=['POST'])
@jwt_required()
def start_study_session():
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    course_id = data.get('course_id')  # Optional
    session_type = data.get('session_type', 'general')
    
    # If course_id provided, verify user has access to it
    if course_id:
        course = Course.query.filter_by(id=course_id, user_id=current_user_id).first()
        if not course:
            return jsonify({"error": "Course not found or you don't have access"}), 404
    
    # Create new study session
    session = StudySession(
        user_id=current_user_id,
        course_id=course_id,
        session_type=session_type,
        start_time=datetime.utcnow()
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        "message": "Study session started",
        "session_id": session.id,
        "start_time": session.start_time.isoformat()
    }), 201

# End a study session
@progress_bp.route('/study-session/<int:session_id>/end', methods=['POST'])
@jwt_required()
def end_study_session(session_id):
    current_user_id = get_jwt_identity()
    
    # Verify session exists and belongs to user
    session = StudySession.query.filter_by(id=session_id, user_id=current_user_id).first()
    if not session:
        return jsonify({"error": "Study session not found or you don't have access"}), 404
    
    # If session already ended
    if session.end_time:
        return jsonify({
            "message": "Study session already ended",
            "session_id": session.id,
            "duration_minutes": session.duration_minutes
        }), 200
    
    # End the session
    session.end_session()
    db.session.commit()
    
    # Update daily study time
    today = date.today()
    daily_study = DailyStudy.query.filter_by(
        user_id=current_user_id,
        study_date=today
    ).first()
    
    if daily_study:
        daily_study.total_minutes += session.duration_minutes
    else:
        daily_study = DailyStudy(
            user_id=current_user_id,
            study_date=today,
            total_minutes=session.duration_minutes
        )
        db.session.add(daily_study)
    
    db.session.commit()
    
    return jsonify({
        "message": "Study session ended",
        "session_id": session.id,
        "duration_minutes": session.duration_minutes,
        "end_time": session.end_time.isoformat()
    }), 200

# Get user's weekly study progress
@progress_bp.route('/weekly-progress', methods=['GET'])
@jwt_required()
def get_weekly_progress():
    current_user_id = get_jwt_identity()
    
    # Calculate date range for last 7 days
    end_date = date.today()
    start_date = end_date - timedelta(days=6)
    
    # Query daily study records for the last 7 days
    daily_records = DailyStudy.query.filter(
        DailyStudy.user_id == current_user_id,
        DailyStudy.study_date >= start_date,
        DailyStudy.study_date <= end_date
    ).all()
    
    # Initialize daily data with zeros
    daily_data = {}
    current_date = start_date
    while current_date <= end_date:
        daily_data[current_date.isoformat()] = 0
        current_date += timedelta(days=1)
    
    # Fill in actual data
    for record in daily_records:
        daily_data[record.study_date.isoformat()] = record.total_minutes / 60  # Convert to hours
    
    # Get question confidence distribution
    confidence_counts = {1: 0, 2: 0, 3: 0}
    progress_records = StudyProgress.query.filter_by(user_id=current_user_id).all()
    
    for record in progress_records:
        confidence_counts[record.confidence_level] = confidence_counts.get(record.confidence_level, 0) + 1
    
    # Calculate course performance
    course_performance = []
    courses = Course.query.filter_by(user_id=current_user_id).all()
    
    for course in courses:
        # Get average confidence for questions in this course
        course_progress = StudyProgress.query.filter_by(
            user_id=current_user_id,
            course_id=course.id
        ).all()
        
        if course_progress:
            avg_confidence = sum(p.confidence_level for p in course_progress) / len(course_progress)
            # Scale to percentage (1=33%, 2=66%, 3=100%)
            performance = (avg_confidence / 3) * 100
        else:
            performance = 0
        
        course_performance.append({
            'id': course.id,
            'title': course.title,
            'performance': round(performance, 1)
        })
    
    # Calculate total study hours for the week
    total_hours = sum(daily_data.values())
    
    # Calculate current study streak
    streak = 0
    current_date = end_date
    while True:
        daily_record = DailyStudy.query.filter_by(
            user_id=current_user_id,
            study_date=current_date
        ).first()
        
        if daily_record and daily_record.total_minutes > 0:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return jsonify({
        "weekly_data": {
            "labels": list(daily_data.keys()),
            "values": list(daily_data.values())
        },
        "confidence_distribution": {
            "low": confidence_counts.get(1, 0),
            "medium": confidence_counts.get(2, 0),
            "high": confidence_counts.get(3, 0)
        },
        "course_performance": course_performance,
        "total_hours": round(total_hours, 1),
        "streak": streak
    }), 200

# Get user's todos
@progress_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    current_user_id = get_jwt_identity()
    
    todos = Todo.query.filter_by(user_id=current_user_id).order_by(Todo.created_at.desc()).all()
    
    result = []
    for todo in todos:
        result.append({
            'id': todo.id,
            'text': todo.text,
            'completed': todo.completed,
            'course_id': todo.course_id,
            'due_date': todo.due_date.isoformat() if todo.due_date else None,
            'created_at': todo.created_at.isoformat()
        })
    
    return jsonify(result), 200

# Create a new todo
@progress_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({"error": "Text is required"}), 400
    
    course_id = data.get('course_id')
    due_date_str = data.get('due_date')
    
    # Parse due date if provided
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    # Create new todo
    todo = Todo(
        user_id=current_user_id,
        course_id=course_id,
        text=data['text'],
        due_date=due_date
    )
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'text': todo.text,
        'completed': todo.completed,
        'course_id': todo.course_id,
        'due_date': todo.due_date.isoformat() if todo.due_date else None,
        'created_at': todo.created_at.isoformat()
    }), 201

# Update todo status
@progress_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    current_user_id = get_jwt_identity()
    
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user_id).first()
    if not todo:
        return jsonify({"error": "Todo not found or you don't have access"}), 404
    
    data = request.get_json()
    if 'completed' in data:
        todo.completed = data['completed']
    if 'text' in data:
        todo.text = data['text']
    if 'due_date' in data:
        if data['due_date']:
            try:
                todo.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        else:
            todo.due_date = None
    
    db.session.commit()
    
    return jsonify({
        'id': todo.id,
        'text': todo.text,
        'completed': todo.completed,
        'course_id': todo.course_id,
        'due_date': todo.due_date.isoformat() if todo.due_date else None,
        'created_at': todo.created_at.isoformat()
    }), 200

# Delete a todo
@progress_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    current_user_id = get_jwt_identity()
    
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user_id).first()
    if not todo:
        return jsonify({"error": "Todo not found or you don't have access"}), 404
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({"message": "Todo deleted successfully"}), 200