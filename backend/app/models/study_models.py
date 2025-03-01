from app.extensions import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    notes = db.relationship('Note', backref='course', lazy=True, cascade="all, delete-orphan")
    practice_questions = db.relationship('PracticeQuestion', backref='course', lazy=True, cascade="all, delete-orphan")
    tests = db.relationship('Test', backref='course', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Course {self.title}>'

class Note(db.Model):
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    def __repr__(self):
        return f'<Note {self.title}>'

class PracticeQuestion(db.Model):
    __tablename__ = 'practice_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    def __repr__(self):
        return f'<PracticeQuestion {self.id}>'

class Test(db.Model):
    __tablename__ = 'tests'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Relationships
    questions = db.relationship('TestQuestion', backref='test', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Test {self.title}>'

class TestQuestion(db.Model):
    __tablename__ = 'test_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON)  # For multiple choice questions
    correct_answer = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, default=1)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    
    def __repr__(self):
        return f'<TestQuestion {self.id}>'

# User study progress tracking
class StudySession(db.Model):
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    def __repr__(self):
        return f'<StudySession {self.id}>'