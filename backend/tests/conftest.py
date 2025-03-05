import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.study_models import Course, Note, PracticeQuestion
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-key'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Create a test user."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.password = 'testpassword'
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def auth_headers(app, test_user):
    """Create authentication headers for the test user."""
    with app.app_context():
        access_token = create_access_token(identity=test_user.id)
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

@pytest.fixture
def test_course(app, test_user):
    """Create a test course."""
    with app.app_context():
        course = Course(
            title='Test Course',
            description='Test Description',
            user_id=test_user.id
        )
        db.session.add(course)
        db.session.commit()
        return course

@pytest.fixture
def test_note(app, test_course):
    """Create a test note."""
    with app.app_context():
        note = Note(
            title='Test Note',
            content='Test Content',
            course_id=test_course.id
        )
        db.session.add(note)
        db.session.commit()
        return note

@pytest.fixture
def test_question(app, test_course):
    """Create a test question."""
    with app.app_context():
        question = PracticeQuestion(
            question='Test Question?',
            answer='Test Answer',
            difficulty='medium',
            course_id=test_course.id
        )
        db.session.add(question)
        db.session.commit()
        return question