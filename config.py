import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class with production support"""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # Use PostgreSQL on Render.com (production), SQLite locally (development)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Render provides postgres:// but SQLAlchemy 1.4+ needs postgresql://
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///' + os.path.join(basedir, 'database', 'car_rental.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Flask configuration
    DEBUG = os.environ.get('FLASK_ENV') != 'production'
    
    # Geofencing settings (in kilometers)
    MAX_ALLOWED_DISTANCE = 50  # km from rental location
    
    # Pricing tiers
    PRICING_TIERS = {
        'economy': 30,    # $ per day
        'luxury': 100,
        'suv': 65
    }
