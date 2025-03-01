from app.extensions import db
from datetime import datetime
import json

class StudyProgress(db.Model):
    """Model for tracking user progress on practice questions."""
    __tablename__ = 'study_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('practice_questions.id'), nullable=False)
    confidence_level = db.Column(db.Integer)  # 1=Low, 2=Medium, 3=High
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<StudyProgress user_id={self.user_id} question_id={self.question_id}>'

class DailyStudy(db.Model):
    """Model for tracking daily study time."""
    __tablename__ = 'daily_study'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_date = db.Column(db.Date, nullable=False)
    total_minutes = db.Column(db.Integer, default=0)  # Total minutes studied
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many DailyStudy records to one User
    user = db.relationship('User', backref='daily_studies')
    
    def __repr__(self):
        return f'<DailyStudy user_id={self.user_id} date={self.study_date} minutes={self.total_minutes}>'

class StudySession(db.Model):
    """Model for tracking individual study sessions."""
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)  # Duration in minutes
    session_type = db.Column(db.String(50), default='general')  # e.g., 'pomodoro', 'notes', 'practice'
    
    # Many StudySession records to one User
    user = db.relationship('User', backref='study_sessions')
    
    # Many StudySession records to one Course (optional)
    course = db.relationship('Course', backref='study_sessions')
    
    def __repr__(self):
        return f'<StudySession user_id={self.user_id} duration={self.duration_minutes}>'
    
    def end_session(self):
        """End the current study session and calculate duration."""
        if not self.end_time:
            self.end_time = datetime.utcnow()
            delta = self.end_time - self.start_time
            self.duration_minutes = int(delta.total_seconds() / 60)

class UserPreference(db.Model):
    """Model for storing user preferences."""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    study_problems = db.Column(db.String(255))  # Comma-separated list of study problems
    pomodoro_work_minutes = db.Column(db.Integer, default=25)
    pomodoro_break_minutes = db.Column(db.Integer, default=5)
    pomodoro_long_break_minutes = db.Column(db.Integer, default=15)
    notification_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # One UserPreference to one User
    user = db.relationship('User', backref=db.backref('preferences', uselist=False))
    
    def __repr__(self):
        return f'<UserPreference user_id={self.user_id}>'
    
    def get_study_problems(self):
        """Return study problems as a list."""
        if not self.study_problems:
            return []
        return self.study_problems.split(',')
    
    def set_study_problems(self, problems_list):
        """Set study problems from a list."""
        if not problems_list:
            self.study_problems = ''
        else:
            self.study_problems = ','.join(problems_list)

class Todo(db.Model):
    """Model for user to-do tasks."""
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    text = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many Todo records to one User
    user = db.relationship('User', backref='todos')
    
    # Many Todo records to one Course (optional)
    course = db.relationship('Course', backref='todos')
    
    def __repr__(self):
        status = "completed" if self.completed else "pending"
        return f'<Todo user_id={self.user_id} text="{self.text[:20]}..." status={status}>'