from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Car(db.Model):
    """Car model representing vehicles in the fleet"""
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    model = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)  # economy, luxury, suv
    status = db.Column(db.String(20), default='available')  # available, booked, in_service, maintenance, out_of_range
    price_tier = db.Column(db.Float, nullable=False)
    
    # GPS Tracker Information (from Abstract Factory)
    tracker_type = db.Column(db.String(50), default='BasicGPS')
    tracker_update_interval = db.Column(db.Integer, default=300)  # seconds
    
    # Location tracking
    current_location_lat = db.Column(db.Float)
    current_location_lng = db.Column(db.Float)
    rental_location_lat = db.Column(db.Float)
    rental_location_lng = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='car', lazy=True)
    claims = db.relationship('Claim', backref='car', lazy=True)
    location_history = db.relationship('LocationHistory', backref='car', lazy=True)
    
    def __repr__(self):
        return f'<Car {self.license_plate} - {self.model}>'


class Booking(db.Model):
    """Booking model for car reservations"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_cnic = db.Column(db.String(15), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    access_code = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.customer_name}>'


class Claim(db.Model):
    """Damage claim model"""
    __tablename__ = 'claims'
    
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
    damage_type = db.Column(db.String(50), nullable=False)  # minor, major, insurance_required
    description = db.Column(db.Text, nullable=False)
    estimated_cost = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, processed
    handler = db.Column(db.String(50))  # Which handler processed it
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Claim {self.id} - {self.damage_type}>'


class LocationHistory(db.Model):
    """Location tracking history"""
    __tablename__ = 'location_history'
    
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    is_out_of_range = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Location {self.car_id} at {self.timestamp}>'


class Admin(UserMixin, db.Model):
    """Admin user model with Flask-Login integration"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'
