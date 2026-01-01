from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    """Abstract base class for pricing strategies"""
    
    @abstractmethod
    def calculate_price(self, base_price, duration_days):
        """Calculate rental price based on strategy"""
        pass
