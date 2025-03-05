import json
import unittest
from app import create_app
from app.extensions import db
from app.models.user import User

class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

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
    
    def tearDown(self):
        """Clean up after the test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_registration(self):
        """Test user registration."""
        # Register a new user
        res = self.client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpassword'
            }),
            content_type='application/json'
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['access_token'])
        self.assertEqual(data['message'], 'User registered successfully')
        
        # Check if the user was actually saved to the database
        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'test@example.com')
    
    def test_duplicate_registration(self):
        """Test that a user cannot register with an existing username."""
        # First registration
        self.client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpassword'
            }),
            content_type='application/json'
        )
        
        # Try to register with the same username
        res = self.client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'another@example.com',
                'password': 'testpassword'
            }),
            content_type='application/json'
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 'Username already exists')
    
    def test_login(self):
        """Test user login."""
        # Register a user
        self.client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpassword'
            }),
            content_type='application/json'
        )
        
        # Login with correct credentials
        res = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'testpassword'
            }),
            content_type='application/json'
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['access_token'])
        self.assertEqual(data['message'], 'Login successful')
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Register a user
        self.client.post(
            '/api/auth/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpassword'
            }),
            content_type='application/json'
        )
        
        # Try to login with wrong password
        res = self.client.post(
            '/api/auth/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'wrongpassword'
            }),
            content_type='application/json'
        )
        
        # Check response
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['error'], 'Invalid username or password')
