from .pricing_strategy import PricingStrategy

class BasePricing(PricingStrategy):
    """Standard pricing with no discounts or surcharges"""
    
    def calculate_price(self, base_price, duration_days):
        """Calculate base price"""
        total = base_price * duration_days
        return {
            'strategy': 'Base Pricing',
            'base_price': base_price,
            'duration_days': duration_days,
            'discount': 0,
            'surcharge': 0,
            'total': total
        }
