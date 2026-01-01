from .car_state import CarState

class InServiceState(CarState):
    """State when car is being serviced"""
    
    def can_book(self):
        return False
    
    def book(self, car):
        print(f"Car {car.license_plate} is in service and cannot be booked")
    
    def complete_service(self, car):
        """Complete service, transition to available"""
        from .available import AvailableState
        car.set_state(AvailableState())
        print(f"Service completed for {car.license_plate}, now available")
    
    def start_maintenance(self, car):
        """Transition to maintenance"""
        from .maintenance import MaintenanceState
        car.set_state(MaintenanceState())
        print(f"Car {car.license_plate} moved from service to maintenance")
    
    def get_state_name(self):
        return "in_service"
