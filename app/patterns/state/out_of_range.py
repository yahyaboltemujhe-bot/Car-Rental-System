from .car_state import CarState

class OutOfRangeState(CarState):
    """State when car is outside allowed geographical zone"""
    
    def can_book(self):
        return False
    
    def book(self, car):
        print(f"Car {car.license_plate} is out of range and cannot be booked")
    
    def complete_service(self, car):
        """Car returned to range, transition to available"""
        from .available import AvailableState
        car.set_state(AvailableState())
        print(f"Car {car.license_plate} returned to allowed zone, now available")
    
    def start_maintenance(self, car):
        print(f"Car {car.license_plate} is out of range, cannot start maintenance")
    
    def get_state_name(self):
        return "out_of_range"
