from .pricing_strategy import PricingStrategy

class PeakPricing(PricingStrategy):
    """Peak season pricing with 25% surcharge"""
    
    SURCHARGE_RATE = 0.25  # 25% surcharge
    
    def calculate_price(self, base_price, duration_days):
        """Calculate price with peak season surcharge"""
        subtotal = base_price * duration_days
        surcharge = subtotal * self.SURCHARGE_RATE
        total = subtotal + surcharge
        
        return {
            'strategy': 'Peak Season Pricing',
            'base_price': base_price,
            'duration_days': duration_days,
            'discount': 0,
            'surcharge': surcharge,
            'total': total,
            'note': 'Peak season 25% surcharge applied'
        }
