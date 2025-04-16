import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_SECURE = False  # Enable this in production with HTTPS
    DATABASE_URL = os.getenv('DATABASE_URL')

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("DATABASE_HOST")
    DB_PORT = os.getenv("DATABASE_PORT")

    IDP_DB_NAME = os.getenv("IDP_DB")
    APP_DB_NAME = os.getenv("APP_DB")

    CLIENT_SECRET = "Long and good secret"
    CLIENT_ID = os.getenv("CLIENT_ID")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")