import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db:5432/app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    