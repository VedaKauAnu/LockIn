import json
import unittest
from unittest.mock import patch
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course, Note
from flask_jwt_extended import create_access_token

class NotesTestCase(unittest.TestCase):
    """Test case for the notes blueprint."""

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
    
    def test_create_note(self):
        """Test note creation."""
        res = self.client.post(
            f'/api/course/{self.course.id}/notes',
            headers=self.headers,
            data=json.dumps({
                'title': 'Test Note',
                'content': 'This is a test note'
            })
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['title'], 'Test Note')
        self.assertEqual(data['content'], 'This is a test note')
        
        # Verify the note was saved to the database
        with self.app.app_context():
            note = Note.query.filter_by(title='Test Note').first()
            self.assertIsNotNone(note)
            self.assertEqual(note.course_id, self.course.id)
    
    def test_get_notes(self):
        """Test getting all notes for a course."""
        # Create some test notes
        with self.app.app_context():
            note1 = Note(title='Note 1', content='Content 1', course_id=self.course.id)
            note2 = Note(title='Note 2', content='Content 2', course_id=self.course.id)
            db.session.add_all([note1, note2])
            db.session.commit()
        
        # Get all notes
        res = self.client.get(f'/api/course/{self.course.id}/notes', headers=self.headers)
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'Note 1')
        self.assertEqual(data[1]['title'], 'Note 2')
    
    @patch('app.ai_service.AIService.generate_notes')
    def test_generate_notes(self, mock_generate_notes):
        """Test generating notes with AI."""
        # Mock the AI service response
        mock_generate_notes.return_value = "These are AI-generated notes about the test topic."
        
        # Generate notes
        res = self.client.post(
            f'/api/course/{self.course.id}/generate-notes',
            headers=self.headers,
            data=json.dumps({
                'topic': 'Test Topic',
                'detail_level': 'medium'
            })
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['title'], 'Notes: Test Topic')
        self.assertEqual(data['content'], "These are AI-generated notes about the test topic.")
        
        # Verify the note was saved to the database
        with self.app.app_context():
            note = Note.query.filter_by(title='Notes: Test Topic').first()
            self.assertIsNotNone(note)
            self.assertEqual(note.content, "These are AI-generated notes about the test topic.")
