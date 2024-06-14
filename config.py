import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dog_park_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOMTOM_API_KEY = os.environ.get('TOMTOM_API_KEY') or 'yUGbsBJgrgWF4EURxpd4xzLhNLAyR409'
