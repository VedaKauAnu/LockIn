import json
import unittest
from unittest.mock import patch
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course, PracticeQuestion
from flask_jwt_extended import create_access_token

class QuestionsTestCase(unittest.TestCase):
    """Test case for the questions blueprint."""

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
            
            # Create a test course
            self.course = Course(title='Test Course', description='Test Description', user_id=self.user.id)
            db.session.add(self.course)
            
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
    
    def test_create_question(self):
        """Test question creation."""
        res = self.client.post(
            f'/api/course/{self.course.id}/questions',
            headers=self.headers,
            data=json.dumps({
                'question': 'Test Question?',
                'answer': 'Test Answer',
                'difficulty': 'medium'
            })
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['question'], 'Test Question?')
        self.assertEqual(data['answer'], 'Test Answer')
        self.assertEqual(data['difficulty'], 'medium')
        
        # Verify the question was saved to the database
        with self.app.app_context():
            question = PracticeQuestion.query.filter_by(question='Test Question?').first()
            self.assertIsNotNone(question)
            self.assertEqual(question.course_id, self.course.id)
    
    def test_get_questions(self):
        """Test getting all questions for a course."""
        # Create some test questions
        with self.app.app_context():
            q1 = PracticeQuestion(question='Q1?', answer='A1', difficulty='easy', course_id=self.course.id)
            q2 = PracticeQuestion(question='Q2?', answer='A2', difficulty='hard', course_id=self.course.id)
            db.session.add_all([q1, q2])
            db.session.commit()
        
        # Get all questions
        res = self.client.get(f'/api/course/{self.course.id}/questions', headers=self.headers)
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['question'], 'Q1?')
        self.assertEqual(data[1]['question'], 'Q2?')