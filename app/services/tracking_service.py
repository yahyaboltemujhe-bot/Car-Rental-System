from app.data.car_repository import CarRepository
from app.models import db, LocationHistory
from app.patterns.observer.subject import Subject
from app.patterns.observer.admin_notifier import AdminNotifier
from app.patterns.observer.alert_logger import AlertLogger
from app.domain.location import Location
from config import Config
from datetime import datetime

class TrackingService:
    """Service for tracking car locations and detecting out-of-range vehicles"""
    
    def __init__(self):
        self.notification_system = Subject()
        # Attach observers (Observer Pattern)
        self.notification_system.attach(AdminNotifier())
        self.notification_system.attach(AlertLogger())
        self.max_distance = Config.MAX_ALLOWED_DISTANCE
    
    def update_location(self, car_id, latitude, longitude):
        """Update car location and check for out-of-range"""
        car = CarRepository.get_by_id(car_id)
        if not car:
            return {'success': False, 'message': 'Car not found'}
        
        # Update current location
        CarRepository.update_location(car_id, latitude, longitude)
        
        # Save to location history
        location_record = LocationHistory(
            car_id=car_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=datetime.now()
        )
        
        # Check if out of range
        if car.rental_location_lat and car.rental_location_lng:
            car_domain = CarRepository.to_domain(car)
            is_out_of_range = car_domain.is_out_of_range(self.max_distance)
            
            location_record.is_out_of_range = is_out_of_range
            
            if is_out_of_range and car.status != 'out_of_range':
                # Car just went out of range
                CarRepository.update_status(car_id, 'out_of_range')
                
                # Send alert with comprehensive vehicle details
                self.notification_system.notify('car_out_of_range', {
                    'car_id': car_id,
                    'license_plate': car.license_plate,
                    'model': car.model,
                    'category': car.category,
                    'tracker_type': car.tracker_type or 'BasicGPS',
                    'distance': car_domain.calculate_distance_from_rental(),
                    'max_allowed': self.max_distance,
                    'current_location': (latitude, longitude),
                    'rental_location': (car.rental_location_lat, car.rental_location_lng)
                })
            
            elif not is_out_of_range and car.status == 'out_of_range':
                # Car returned to range
                CarRepository.update_status(car_id, 'booked')  # or available
                
                self.notification_system.notify('car_returned_to_range', {
                    'car_id': car_id,
                    'license_plate': car.license_plate,
                    'model': car.model
                })
        
        db.session.add(location_record)
        db.session.commit()
        
        return {
            'success': True,
            'location': {
                'latitude': location_record.latitude,
                'longitude': location_record.longitude,
                'timestamp': location_record.timestamp.isoformat(),
                'is_out_of_range': location_record.is_out_of_range
            },
            'is_out_of_range': location_record.is_out_of_range
        }
    
    def get_location_history(self, car_id, limit=50):
        """Get location history for a car"""
        return LocationHistory.query.filter_by(car_id=car_id)\
            .order_by(LocationHistory.timestamp.desc())\
            .limit(limit).all()
    
    def get_out_of_range_cars(self):
        """Get all cars currently out of range"""
        return CarRepository.get_by_status('out_of_range')
