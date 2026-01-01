from .car_state import CarState

class MaintenanceState(CarState):
    """State when car is under maintenance"""
    
    def can_book(self):
        return False
    
    def book(self, car):
        print(f"Car {car.license_plate} is under maintenance and cannot be booked")
    
    def complete_service(self, car):
        """Complete maintenance, transition to available"""
        from .available import AvailableState
        car.set_state(AvailableState())
        print(f"Maintenance completed for {car.license_plate}, now available")
    
    def start_maintenance(self, car):
        print(f"Car {car.license_plate} is already under maintenance")
    
    def get_state_name(self):
        return "maintenance"
