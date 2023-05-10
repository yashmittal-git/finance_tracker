import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'finance_tracker.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'development'
