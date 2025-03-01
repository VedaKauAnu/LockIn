from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.ai_service import AIService

strategies_bp = Blueprint('strategies', __name__)
ai_service = AIService()

@strategies_bp.route('/test-strategies', methods=['POST'])
@jwt_required()
def get_test_strategies():
    """
    Generate personalized test-taking strategies based on user input
    """
    current_user_id = get_jwt_identity()
    
    # Get the user to personalize strategies
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if not data or not data.get('test_type'):
        return jsonify({"error": "Test type is required"}), 400
    
    test_type = data.get('test_type')
    student_problems = data.get('problems', [])
    
    try:
        # Generate test strategies using AI service
        strategies = ai_service.generate_test_strategies(
            test_type=test_type,
            student_problems=student_problems
        )
        
        return jsonify({
            'test_type': test_type,
            'strategies': strategies
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500