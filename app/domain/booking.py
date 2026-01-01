from datetime import datetime
import secrets

class Booking:
    """Booking domain entity"""
    
    def __init__(self, booking_id, car_id, customer_name, customer_phone, 
                 customer_cnic, start_date, end_date, total_amount):
        self.id = booking_id
        self.car_id = car_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_cnic = customer_cnic
        self.start_date = start_date
        self.end_date = end_date
        self.total_amount = total_amount
        self.status = 'active'
        self.access_code = self._generate_access_code()
    
    def _generate_access_code(self):
        """Generate unique access code for car access"""
        return secrets.token_urlsafe(8)
    
    def calculate_duration_days(self):
        """Calculate booking duration in days"""
        delta = self.end_date - self.start_date
        return max(1, delta.days)  # Minimum 1 day
    
    def is_active(self):
        """Check if booking is currently active"""
        now = datetime.now()
        return (self.status == 'active' and 
                self.start_date <= now <= self.end_date)
    
    def complete(self):
        """Mark booking as completed"""
        self.status = 'completed'
    
    def cancel(self):
        """Cancel the booking"""
        self.status = 'cancelled'
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.customer_name} - {self.status}>'
