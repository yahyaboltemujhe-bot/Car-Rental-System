from .vehicle_factory import VehicleFactory

class EconomyVehicleFactory(VehicleFactory):
    """Factory for creating economy vehicles and their components"""
    
    def create_car(self):
        """Create an economy car"""
        return {
            'category': 'economy',
            'features': ['Manual transmission', 'Basic audio', 'Standard seats'],
            'fuel_efficiency': 'High (40+ MPG)',
            'price_tier': 30
        }
    
    def create_tracker(self):
        """Create basic GPS tracker for economy vehicles"""
        return {
            'type': 'BasicGPS',
            'update_interval': 300,  # 5 minutes
            'features': ['Location tracking']
        }
    
    def create_access_system(self):
        """Create basic access system"""
        return {
            'type': 'KeyAccess',
            'features': ['Physical key', 'Basic alarm']
        }
    
    def create_maintenance_profile(self):
        """Create economy maintenance profile"""
        return {
            'interval_km': 5000,
            'service_type': 'Basic',
            'estimated_cost': 100
        }
