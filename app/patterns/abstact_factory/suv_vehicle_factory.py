from .vehicle_factory import VehicleFactory

class SUVVehicleFactory(VehicleFactory):
    """Factory for creating SUV vehicles and their components"""
    
    def create_car(self):
        """Create an SUV"""
        return {
            'category': 'suv',
            'features': [
                'Automatic/Manual transmission',
                'Premium audio',
                'Spacious interior',
                '4WD/AWD capability',
                'Roof rack'
            ],
            'fuel_efficiency': 'Low (18-22 MPG)',
            'price_tier': 65
        }
    
    def create_tracker(self):
        """Create rugged GPS tracker for SUVs"""
        return {
            'type': 'RuggedGPS',
            'update_interval': 120,  # 2 minutes
            'features': [
                'Real-time location',
                'Off-road tracking',
                'Altitude monitoring',
                'Geofencing'
            ]
        }
    
    def create_access_system(self):
        """Create robust access system for SUVs"""
        return {
            'type': 'SmartKeyAccess',
            'features': [
                'Smart key',
                'Remote unlock',
                'Push-button start',
                'Alarm system'
            ]
        }
    
    def create_maintenance_profile(self):
        """Create SUV maintenance profile"""
        return {
            'interval_km': 7500,
            'service_type': 'Standard Plus',
            'estimated_cost': 300
        }
