import json
import unittest
from datetime import datetime, date, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course, PracticeQuestion
from app.models.progress_models import StudyProgress, DailyStudy, StudySession, Todo
from flask_jwt_extended import create_access_token

class ProgressTestCase(unittest.TestCase):
    """Test case for the progress blueprint."""

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
            
            # Create a test question
            self.question = PracticeQuestion(
                question='Test Question?', 
                answer='Test Answer', 
                difficulty='medium', 
                course_id=self.course.id
            )
            db.session.add(self.question)
            
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
    
    def test_record_question_progress(self):
        """Test recording question progress."""
        res = self.client.post(
            '/api/question-progress',
            headers=self.headers,
            data=json.dumps({
                'question_id': self.question.id,
                'confidence_level': 2
            })
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question_id'], self.question.id)
        self.assertEqual(data['confidence_level'], 2)
        
        # Verify the progress was saved to the database
        with self.app.app_context():
            progress = StudyProgress.query.filter_by(
                user_id=self.user.id,
                question_id=self.question.id
            ).first()
            self.assertIsNotNone(progress)
            self.assertEqual(progress.confidence_level, 2)
    
    def test_start_study_session(self):
        """Test starting a study session."""
        res = self.client.post(
            '/api/study-session/start',
            headers=self.headers,
            data=json.dumps({
                'course_id': self.course.id,
                'session_type': 'focused'
            })
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['message'], 'Study session started')
        self.assertTrue('session_id' in data)
        
        # Verify the session was created in the database
        with self.app.app_context():
            session = StudySession.query.get(data['session_id'])
            self.assertIsNotNone(session)
            self.assertEqual(session.user_id, self.user.id)
            self.assertEqual(session.course_id, self.course.id)
            self.assertEqual(session.session_type, 'focused')
    
    def test_end_study_session(self):
        """Test ending a study session."""
        # Start a session
        with self.app.app_context():
            session = StudySession(
                user_id=self.user.id,
                course_id=self.course.id,
                session_type='general',
                start_time=datetime.utcnow() - timedelta(minutes=30)  # Started 30 minutes ago
            )
            db.session.add(session)
            db.session.commit()
            session_id = session.id
        
        # End the session
        res = self.client.post(
            f'/api/study-session/{session_id}/end',
            headers=self.headers
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Study session ended')
        self.assertEqual(data['session_id'], session_id)
        
        # Verify session was updated in the database
        with self.app.app_context():
            updated_session = StudySession.query.get(session_id)
            self.assertIsNotNone(updated_session.end_time)
            self.assertIsNotNone(updated_session.duration_minutes)
            
            # Check that a daily study record was created
            daily_study = DailyStudy.query.filter_by(
                user_id=self.user.id,
                study_date=date.today()
            ).first()
            self.assertIsNotNone(daily_study)
            self.assertEqual(daily_study.total_minutes, updated_session.duration_minutes)

if __name__ == '__main__':
    unittest.main()