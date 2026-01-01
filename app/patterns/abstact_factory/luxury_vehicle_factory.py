from .vehicle_factory import VehicleFactory

class LuxuryVehicleFactory(VehicleFactory):
    """Factory for creating luxury vehicles and their components"""
    
    def create_car(self):
        """Create a luxury car"""
        return {
            'category': 'luxury',
            'features': [
                'Automatic transmission',
                'Premium sound system',
                'Leather seats',
                'Climate control',
                'Advanced safety features'
            ],
            'fuel_efficiency': 'Medium (25-30 MPG)',
            'price_tier': 100
        }
    
    def create_tracker(self):
        """Create advanced GPS tracker for luxury vehicles"""
        return {
            'type': 'AdvancedGPS',
            'update_interval': 60,  # 1 minute
            'features': [
                'Real-time location',
                'Speed monitoring',
                'Geofencing',
                'Route history'
            ]
        }
    
    def create_access_system(self):
        """Create premium keyless access system"""
        return {
            'type': 'KeylessAccess',
            'features': [
                'Smartphone unlock',
                'Biometric verification',
                'Remote start',
                'Advanced security'
            ]
        }
    
    def create_maintenance_profile(self):
        """Create luxury maintenance profile"""
        return {
            'interval_km': 10000,
            'service_type': 'Premium',
            'estimated_cost': 500
        }
