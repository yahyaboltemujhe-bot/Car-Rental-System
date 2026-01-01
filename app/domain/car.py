from math import radians, sin, cos, sqrt, atan2

class Car:
    """Car domain entity with state management"""
    
    def __init__(self, car_id, license_plate, model, category, state=None):
        self.id = car_id
        self.license_plate = license_plate
        self.model = model
        self.category = category  # economy, luxury, suv
        self._state = state  # State pattern object
        self.current_location = None
        self.rental_location = None
    
    def set_state(self, state):
        """Set the current state of the car"""
        self._state = state
    
    def get_state(self):
        """Get the current state"""
        return self._state
    
    def can_be_booked(self):
        """Check if car can be booked (delegates to state)"""
        if self._state:
            return self._state.can_book()
        return False
    
    def book(self):
        """Attempt to book the car"""
        if self._state:
            self._state.book(self)
    
    def complete_service(self):
        """Complete service and return to available"""
        if self._state:
            self._state.complete_service(self)
    
    def start_maintenance(self):
        """Start maintenance on the car"""
        if self._state:
            self._state.start_maintenance(self)
    
    def calculate_distance_from_rental(self):
        """Calculate distance from rental location in kilometers"""
        if not self.current_location or not self.rental_location:
            return 0
        
        lat1, lon1 = self.rental_location
        lat2, lon2 = self.current_location
        
        # Haversine formula
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def is_out_of_range(self, max_distance):
        """Check if car is beyond allowed distance"""
        return self.calculate_distance_from_rental() > max_distance
    
    def __repr__(self):
        state_name = self._state.__class__.__name__ if self._state else 'NoState'
        return f'<Car {self.license_plate} - {state_name}>'
