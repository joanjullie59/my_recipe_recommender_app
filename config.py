import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'simple'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
