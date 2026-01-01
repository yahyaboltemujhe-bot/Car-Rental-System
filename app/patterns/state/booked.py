from .car_state import CarState

class BookedState(CarState):
    """State when car is currently booked"""
    
    def can_book(self):
        return False
    
    def book(self, car):
        print(f"Car {car.license_plate} is already booked")
    
    def complete_service(self, car):
        """Return booking, transition to available"""
        from .available import AvailableState
        car.set_state(AvailableState())
        print(f"Booking completed for {car.license_plate}, now available")
    
    def start_maintenance(self, car):
        print(f"Cannot start maintenance on booked car {car.license_plate}")
    
    def get_state_name(self):
        return "booked"
