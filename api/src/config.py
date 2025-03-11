import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Enable this in production with HTTPS
    SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME')
    DATABASE_URL = os.getenv('DATABASE_URL')
