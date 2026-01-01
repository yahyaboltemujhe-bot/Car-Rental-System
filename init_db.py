"""
Database initialization script
Creates all tables and adds sample data for testing
"""

from app import create_app
from app.models import db, Car, Admin, Booking, Claim, LocationHistory
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def init_database():
    """Initialize database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating tables...")
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = Admin(
            username='admin',
            email='admin@carrent.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample cars
        print("Adding sample cars...")
        cars = [
            Car(
                model='Toyota Corolla 2023',
                category='economy',
                license_plate='ABC-123',
                price_tier=3000.0,
                status='available',
                current_location_lat=33.6844,
                current_location_lng=73.0479,
                rental_location_lat=33.6844,
                rental_location_lng=73.0479
            ),
            Car(
                model='Honda Civic 2023',
                category='economy',
                license_plate='XYZ-789',
                price_tier=3500.0,
                status='available',
                current_location_lat=33.6844,
                current_location_lng=73.0479,
                rental_location_lat=33.6844,
                rental_location_lng=73.0479
            ),
            Car(
                model='Mercedes E-Class 2024',
                category='luxury',
                license_plate='LUX-001',
                price_tier=15000.0,
                status='available',
                current_location_lat=33.6844,
                current_location_lng=73.0479,
                rental_location_lat=33.6844,
                rental_location_lng=73.0479
            ),
            Car(
                model='Toyota Land Cruiser 2024',
                category='suv',
                license_plate='SUV-100',
                price_tier=12000.0,
                status='available',
                current_location_lat=33.6844,
                current_location_lng=73.0479,
                rental_location_lat=33.6844,
                rental_location_lng=73.0479
            ),
        ]
        
        for car in cars:
            db.session.add(car)
        
        db.session.commit()
        
        print("Database initialized successfully!")
        print("\nAdmin credentials:")
        print("Username: admin")
        print("Password: admin123")
        print(f"\n{len(cars)} sample cars added")
        print("\nRun the application with: python run.py")

if __name__ == '__main__':
    init_database()
