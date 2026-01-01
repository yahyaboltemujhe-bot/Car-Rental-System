from app.data.booking_repository import BookingRepository
from app.data.car_repository import CarRepository
from app.patterns.observer.subject import Subject
from datetime import datetime

class BookingService:
    """Service for managing bookings using State and Observer patterns"""
    
    def __init__(self):
        self.notification_system = Subject()
    
    def create_booking(self, car_id, customer_name, customer_phone, customer_cnic,
                      start_date, end_date, pricing_strategy='base'):
        """Create a new booking"""
        # Check if car exists and is available
        car = CarRepository.get_by_id(car_id)
        if not car:
            return {'success': False, 'message': 'Car not found'}
        
        if car.status != 'available':
            return {'success': False, 'message': f'Car is not available (current status: {car.status})'}
        
        # Calculate duration
        duration_days = (end_date - start_date).days
        if duration_days < 1:
            return {'success': False, 'message': 'Rental duration must be at least 1 day'}
        
        # Calculate price (simple calculation)
        total_amount = car.price_tier * duration_days
        price_info = {'total': total_amount}
        
        # Generate access code
        from app.domain.booking import Booking as BookingDomain
        temp_booking = BookingDomain(None, car_id, customer_name, customer_phone,
                                    customer_cnic, start_date, end_date, price_info['total'])
        access_code = temp_booking.access_code
        
        # Create booking
        booking = BookingRepository.create(
            car_id=car_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_cnic=customer_cnic,
            start_date=start_date,
            end_date=end_date,
            total_amount=price_info['total'],
            access_code=access_code
        )
        
        # Update car status to booked
        CarRepository.update_status(car_id, 'booked')
        
        # Notify observers
        self.notification_system.notify('car_booked', {
            'car_id': car_id,
            'license_plate': car.license_plate,
            'customer_name': customer_name,
            'booking_id': booking.id
        })
        
        return {
            'success': True,
            'booking': booking,
            'price_info': price_info,
            'access_code': access_code
        }
    
    def complete_booking(self, booking_id):
        """Complete a booking and return car to available"""
        booking = BookingRepository.get_by_id(booking_id)
        if not booking:
            return {'success': False, 'message': 'Booking not found'}
        
        # Update booking status
        BookingRepository.update_status(booking_id, 'completed')
        
        # Update car status back to available
        car = CarRepository.update_status(booking.car_id, 'available')
        
        # Notify observers
        self.notification_system.notify('booking_completed', {
            'booking_id': booking_id,
            'car_id': booking.car_id,
            'license_plate': car.license_plate if car else 'Unknown'
        })
        
        return {'success': True, 'message': 'Booking completed successfully'}
    
    def cancel_booking(self, booking_id):
        """Cancel a booking"""
        booking = BookingRepository.get_by_id(booking_id)
        if not booking:
            return {'success': False, 'message': 'Booking not found'}
        
        BookingRepository.update_status(booking_id, 'cancelled')
        CarRepository.update_status(booking.car_id, 'available')
        
        return {'success': True, 'message': 'Booking cancelled successfully'}
    
    def get_all_bookings(self):
        """Get all bookings"""
        return BookingRepository.get_all()
    
    def get_booking_by_id(self, booking_id):
        """Get booking by ID"""
        return BookingRepository.get_by_id(booking_id)
    
    def get_active_bookings(self):
        """Get active bookings"""
        return BookingRepository.get_active_bookings()
    
    def verify_access_code(self, access_code):
        """Verify booking access code"""
        return BookingRepository.get_by_access_code(access_code)
