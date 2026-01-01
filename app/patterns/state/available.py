from .car_state import CarState

class AvailableState(CarState):
    """State when car is available for booking"""
    
    def can_book(self):
        return True
    
    def book(self, car):
        """Transition to booked state"""
        from .booked import BookedState
        car.set_state(BookedState())
        print(f"Car {car.license_plate} is now booked")
    
    def complete_service(self, car):
        print(f"Car {car.license_plate} is already available")
    
    def start_maintenance(self, car):
        """Transition to maintenance state"""
        from .maintenance import MaintenanceState
        car.set_state(MaintenanceState())
        print(f"Car {car.license_plate} is now under maintenance")
    
    def get_state_name(self):
        return "available"
