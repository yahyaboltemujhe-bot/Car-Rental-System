from app.models import db, Car
from app.domain.car import Car as CarDomain
from app.patterns.state.available import AvailableState
from app.patterns.state.booked import BookedState
from app.patterns.state.in_service import InServiceState
from app.patterns.state.maintenance import MaintenanceState
from app.patterns.state.out_of_range import OutOfRangeState

class CarRepository:
    """Repository for car data access"""
    
    STATE_MAP = {
        'available': AvailableState,
        'booked': BookedState,
        'in_service': InServiceState,
        'maintenance': MaintenanceState,
        'out_of_range': OutOfRangeState
    }
    
    @staticmethod
    def create(license_plate, model, category, price_tier, tracker_type='BasicGPS', 
               tracker_update_interval=300, rental_lat=None, rental_lng=None):
        """Create a new car with tracker"""
        car = Car(
            license_plate=license_plate,
            model=model,
            category=category,
            price_tier=price_tier,
            status='available',
            tracker_type=tracker_type,
            tracker_update_interval=tracker_update_interval,
            rental_location_lat=rental_lat,
            rental_location_lng=rental_lng
        )
        db.session.add(car)
        db.session.commit()
        return car
    
    @staticmethod
    def get_by_id(car_id):
        """Get car by ID"""
        return Car.query.get(car_id)
    
    @staticmethod
    def get_all():
        """Get all cars"""
        return Car.query.all()
    
    @staticmethod
    def get_by_status(status):
        """Get cars by status"""
        return Car.query.filter_by(status=status).all()
    
    @staticmethod
    def get_available_cars():
        """Get all available cars"""
        return Car.query.filter_by(status='available').all()
    
    @staticmethod
    def update_status(car_id, new_status):
        """Update car status"""
        car = Car.query.get(car_id)
        if car:
            car.status = new_status
            db.session.commit()
        return car
    
    @staticmethod
    def update_location(car_id, latitude, longitude):
        """Update car's current location"""
        car = Car.query.get(car_id)
        if car:
            car.current_location_lat = latitude
            car.current_location_lng = longitude
            db.session.commit()
        return car
    
    @staticmethod
    def delete(car_id):
        """Delete a car"""
        car = Car.query.get(car_id)
        if car:
            db.session.delete(car)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def to_domain(car_model):
        """Convert database model to domain entity"""
        if not car_model:
            return None
        
        car_domain = CarDomain(
            car_id=car_model.id,
            license_plate=car_model.license_plate,
            model=car_model.model,
            category=car_model.category
        )
        
        # Set the appropriate state
        state_class = CarRepository.STATE_MAP.get(car_model.status, AvailableState)
        car_domain.set_state(state_class())
        
        # Set locations
        if car_model.current_location_lat and car_model.current_location_lng:
            car_domain.current_location = (car_model.current_location_lat, car_model.current_location_lng)
        
        if car_model.rental_location_lat and car_model.rental_location_lng:
            car_domain.rental_location = (car_model.rental_location_lat, car_model.rental_location_lng)
        
        return car_domain
