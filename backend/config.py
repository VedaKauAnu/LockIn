import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development config."""
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')

class TestingConfig(Config):
    """Testing config."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProductionConfig(Config):
    """Production config."""
    FLASK_ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
# Dictionary with possible configurations
config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)