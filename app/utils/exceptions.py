"""
Custom exception classes for better error handling
"""

class CarRentalException(Exception):
    """Base exception for all car rental system errors"""
    status_code = 500
    
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error'] = self.__class__.__name__
        return rv


class CarNotFoundException(CarRentalException):
    """Raised when a car is not found"""
    status_code = 404
    
    def __init__(self, car_id):
        super().__init__(f'Car with ID {car_id} not found', status_code=404)


class CarNotAvailableException(CarRentalException):
    """Raised when trying to book an unavailable car"""
    status_code = 409
    
    def __init__(self, car_id, current_status):
        super().__init__(
            f'Car {car_id} is not available (current status: {current_status})',
            status_code=409
        )


class BookingNotFoundException(CarRentalException):
    """Raised when a booking is not found"""
    status_code = 404
    
    def __init__(self, booking_id):
        super().__init__(f'Booking with ID {booking_id} not found', status_code=404)


class InvalidBookingDatesException(CarRentalException):
    """Raised when booking dates are invalid"""
    status_code = 400
    
    def __init__(self, message):
        super().__init__(message, status_code=400)


class UnauthorizedAccessException(CarRentalException):
    """Raised when access code verification fails"""
    status_code = 403
    
    def __init__(self):
        super().__init__('Invalid access code', status_code=403)


class ValidationException(CarRentalException):
    """Raised when input validation fails"""
    status_code = 400
    
    def __init__(self, field, message):
        super().__init__(f'{field}: {message}', status_code=400)
        self.field = field


class DatabaseException(CarRentalException):
    """Raised when database operations fail"""
    status_code = 500
    
    def __init__(self, operation, details):
        super().__init__(
            f'Database {operation} failed: {details}',
            status_code=500
        )


class PaymentException(CarRentalException):
    """Raised when payment processing fails"""
    status_code = 402
    
    def __init__(self, message):
        super().__init__(f'Payment failed: {message}', status_code=402)
