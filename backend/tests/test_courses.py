import json
import unittest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course
from flask_jwt_extended import create_access_token

class CoursesTestCase(unittest.TestCase):
    """Test case for the courses blueprint."""

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
    
    def test_create_course(self):
        """Test course creation."""
        res = self.client.post(
            '/api/courses/',
            headers=self.headers,
            data=json.dumps({
                'title': 'Test Course',
                'description': 'This is a test course'
            })
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['title'], 'Test Course')
        self.assertEqual(data['description'], 'This is a test course')
        
        # Verify the course was saved to the database
        with self.app.app_context():
            course = Course.query.filter_by(title='Test Course').first()
            self.assertIsNotNone(course)
            self.assertEqual(course.user_id, self.user.id)
    
    def test_get_courses(self):
        """Test getting all courses for a user."""
        # Create some test courses
        with self.app.app_context():
            course1 = Course(title='Course 1', description='Description 1', user_id=self.user.id)
            course2 = Course(title='Course 2', description='Description 2', user_id=self.user.id)
            db.session.add_all([course1, course2])
            db.session.commit()
        
        # Get all courses
        res = self.client.get('/api/courses/', headers=self.headers)
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['title'], 'Course 1')
        self.assertEqual(data[1]['title'], 'Course 2')
    
    def test_get_course(self):
        """Test getting a specific course."""
        # Create a test course
        with self.app.app_context():
            course = Course(title='Test Course', description='Test Description', user_id=self.user.id)
            db.session.add(course)
            db.session.commit()
            course_id = course.id
        
        # Get the course
        res = self.client.get(f'/api/courses/{course_id}', headers=self.headers)
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['title'], 'Test Course')
        self.assertEqual(data['description'], 'Test Description')
    
    def test_update_course(self):
        """Test updating a course."""
        # Create a test course
        with self.app.app_context():
            course = Course(title='Old Title', description='Old Description', user_id=self.user.id)
            db.session.add(course)
            db.session.commit()
            course_id = course.id
        
        # Update the course
        res = self.client.put(
            f'/api/courses/{course_id}',
            headers=self.headers,
            data=json.dumps({
                'title': 'New Title',
                'description': 'New Description'
            })
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['title'], 'New Title')
        self.assertEqual(data['description'], 'New Description')
        
        # Verify the update in the database
        with self.app.app_context():
            updated_course = Course.query.get(course_id)
            self.assertEqual(updated_course.title, 'New Title')
            self.assertEqual(updated_course.description, 'New Description')
    
    def test_delete_course(self):
        """Test deleting a course."""
        # Create a test course
        with self.app.app_context():
            course = Course(title='Test Course', description='Test Description', user_id=self.user.id)
            db.session.add(course)
            db.session.commit()
            course_id = course.id
        
        # Delete the course
        res = self.client.delete(f'/api/courses/{course_id}', headers=self.headers)
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'Course deleted successfully')
        
        # Verify the course was deleted from the database
        with self.app.app_context():
            deleted_course = Course.query.get(course_id)
            self.assertIsNone(deleted_course)