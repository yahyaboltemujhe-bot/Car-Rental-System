from app.models import db, Booking
from datetime import datetime

class BookingRepository:
    """Repository for booking data access"""
    
    @staticmethod
    def create(car_id, customer_name, customer_phone, customer_cnic, 
               start_date, end_date, total_amount, access_code):
        """Create a new booking"""
        booking = Booking(
            car_id=car_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_cnic=customer_cnic,
            start_date=start_date,
            end_date=end_date,
            total_amount=total_amount,
            access_code=access_code,
            status='active'
        )
        db.session.add(booking)
        db.session.commit()
        return booking
    
    @staticmethod
    def get_by_id(booking_id):
        """Get booking by ID"""
        return Booking.query.get(booking_id)
    
    @staticmethod
    def get_all():
        """Get all bookings"""
        return Booking.query.all()
    
    @staticmethod
    def get_active_bookings():
        """Get all active bookings"""
        return Booking.query.filter_by(status='active').all()
    
    @staticmethod
    def get_by_car(car_id):
        """Get all bookings for a specific car"""
        return Booking.query.filter_by(car_id=car_id).all()
    
    @staticmethod
    def get_active_booking_for_car(car_id):
        """Get active booking for a car"""
        return Booking.query.filter_by(car_id=car_id, status='active').first()
    
    @staticmethod
    def update_status(booking_id, new_status):
        """Update booking status"""
        booking = Booking.query.get(booking_id)
        if booking:
            booking.status = new_status
            db.session.commit()
        return booking
    
    @staticmethod
    def get_by_access_code(access_code):
        """Get booking by access code"""
        return Booking.query.filter_by(access_code=access_code).first()
    
    @staticmethod
    def verify_access_code(booking_id, access_code):
        """Verify access code for a booking"""
        booking = Booking.query.get(booking_id)
        if booking and booking.access_code == access_code:
            return True
        return False
