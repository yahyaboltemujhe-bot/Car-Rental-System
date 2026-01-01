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
    
    # Render provides postgres:// — prefer psycopg3 driver for newer Python versions
    # Convert scheme and ensure SQLAlchemy uses psycopg3 (postgresql+psycopg://)
    if DATABASE_URL:
        # Normalize scheme for pg8000 driver
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+pg8000://', 1)
        elif DATABASE_URL.startswith('postgresql://'):
            DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+pg8000://', 1)

        # Convert common query params: translate sslmode -> ssl for pg8000 compatibility
        try:
            from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
            parsed = urlparse(DATABASE_URL)
            qs = dict(parse_qsl(parsed.query))
            if 'sslmode' in qs:
                val = qs.pop('sslmode').lower()
                qs['ssl'] = 'true' if val in ('require', 'verify-full', 'verify-ca') else 'false'
                new_query = urlencode(qs)
                DATABASE_URL = urlunparse(parsed._replace(query=new_query))
        except Exception:
            # If parsing fails, leave DATABASE_URL as-is and let the driver attempt connection
            pass

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///' + os.path.join(basedir, 'database', 'car_rental.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Flask configuration
    # Safer default: only enable DEBUG when FLASK_ENV is explicitly set to 'development'
    DEBUG = os.environ.get('FLASK_ENV', '').lower() == 'development'
    
    # Geofencing settings (in kilometers)
    MAX_ALLOWED_DISTANCE = 50  # km from rental location
    
    # Pricing tiers
    PRICING_TIERS = {
        'economy': 30,    # $ per day
        'luxury': 100,
        'suv': 65
    }
