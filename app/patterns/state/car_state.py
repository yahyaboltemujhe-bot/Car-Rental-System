from abc import ABC, abstractmethod

class CarState(ABC):
    """Abstract base class for car states"""
    
    @abstractmethod
    def can_book(self):
        """Check if car can be booked in this state"""
        pass
    
    @abstractmethod
    def book(self, car):
        """Attempt to book the car"""
        pass
    
    @abstractmethod
    def complete_service(self, car):
        """Complete service and transition state"""
        pass
    
    @abstractmethod
    def start_maintenance(self, car):
        """Start maintenance"""
        pass
    
    @abstractmethod
    def get_state_name(self):
        """Get the name of this state"""
        pass
