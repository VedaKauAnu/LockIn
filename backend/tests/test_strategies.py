import json
import unittest
from unittest.mock import patch
from app import create_app
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token

class StrategiesTestCase(unittest.TestCase):
    """Test case for the strategies blueprint."""

    def setUp(self):
        """Set up test client and initialize test database."""
        self.app = create_app()
        self.app.config.update({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create a test user
            self.user = User(username='testuser', email='test@example.com')
            self.user.password = 'testpassword'
            db.session.add(self.user)
            db.session.commit()
            
            # Create a JWT token for the test user
            self.access_token = create_access_token(identity=self.user.id)
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
    
    def tearDown(self):
        """Clean up after the test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    @patch('app.ai_service.AIService.generate_test_strategies')
    def test_get_test_strategies(self, mock_generate_strategies):
        """Test generating test strategies with AI."""
        # Mock the AI service response
        mock_generate_strategies.return_value = "These are test strategies for multiple-choice exams."
        
        # Generate strategies
        res = self.client.post(
            '/api/test-strategies',
            headers=self.headers,
            data=json.dumps({
                'test_type': 'multiple-choice',
                'problems': ['test anxiety', 'time management']
            })
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['test_type'], 'multiple-choice')
        self.assertEqual(data['strategies'], "These are test strategies for multiple-choice exams.")
        
        # Verify that the AIService was called with the right parameters
        mock_generate_strategies.assert_called_once_with(
            test_type='multiple-choice',
            student_problems=['test anxiety', 'time management']
        )
