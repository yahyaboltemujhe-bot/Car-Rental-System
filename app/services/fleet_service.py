from app.data.car_repository import CarRepository
from app.patterns.abstact_factory.economy_vehicle_factory import EconomyVehicleFactory
from app.patterns.abstact_factory.luxury_vehicle_factory import LuxuryVehicleFactory
from app.patterns.abstact_factory.suv_vehicle_factory import SUVVehicleFactory
from app.patterns.observer.subject import Subject

class FleetService:
    """Service for managing fleet operations using Abstract Factory pattern"""
    
    FACTORY_MAP = {
        'economy': EconomyVehicleFactory,
        'luxury': LuxuryVehicleFactory,
        'suv': SUVVehicleFactory
    }
    
    def __init__(self):
        self.notification_system = Subject()
    
    def add_car(self, license_plate, model, category, rental_lat=None, rental_lng=None):
        """Add a new car to the fleet using appropriate factory"""
        # Get the factory for this category
        factory_class = self.FACTORY_MAP.get(category)
        if not factory_class:
            return {'success': False, 'message': f'Invalid category: {category}'}
        
        factory = factory_class()
        
        # Create car configuration from factory
        car_config = factory.create_car()
        tracker_config = factory.create_tracker()
        access_config = factory.create_access_system()
        maintenance_config = factory.create_maintenance_profile()
        
        # Save to database with tracker information
        car = CarRepository.create(
            license_plate=license_plate,
            model=model,
            category=category,
            price_tier=car_config['price_tier'],
            tracker_type=tracker_config['type'],
            tracker_update_interval=tracker_config['update_interval'],
            rental_lat=rental_lat,
            rental_lng=rental_lng
        )
        
        return {
            'success': True,
            'car': car,
            'config': car_config,
            'tracker': tracker_config,
            'access': access_config,
            'maintenance': maintenance_config
        }
    
    def get_all_cars(self):
        """Get all cars in the fleet"""
        return CarRepository.get_all()
    
    def get_car_by_id(self, car_id):
        """Get a specific car by ID"""
        return CarRepository.get_by_id(car_id)
    
    def get_cars_by_status(self, status):
        """Get cars filtered by status"""
        return CarRepository.get_by_status(status)
    
    def get_available_cars(self):
        """Get all available cars"""
        return CarRepository.get_available_cars()
    
    def update_car_status(self, car_id, new_status):
        """Update car status"""
        car = CarRepository.update_status(car_id, new_status)
        
        # Notify observers of status change
        if car:
            self.notification_system.notify('car_status_changed', {
                'car_id': car_id,
                'license_plate': car.license_plate,
                'new_status': new_status
            })
        
        return car
    
    def get_fleet_statistics(self):
        """Get fleet statistics"""
        all_cars = self.get_all_cars()
        
        stats = {
            'total_cars': len(all_cars),
            'available_cars': len([c for c in all_cars if c.status == 'available']),
            'booked_cars': len([c for c in all_cars if c.status == 'booked']),
            'in_service_cars': len([c for c in all_cars if c.status == 'in_service']),
            'maintenance_cars': len([c for c in all_cars if c.status == 'maintenance']),
            'out_of_range_cars': len([c for c in all_cars if c.status == 'out_of_range'])
        }
        
        return stats
