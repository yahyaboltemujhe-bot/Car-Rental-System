from .pricing_strategy import PricingStrategy

class DiscountPricing(PricingStrategy):
    """Discount pricing for long-term rentals"""
    
    def calculate_price(self, base_price, duration_days):
        """Calculate price with tiered discounts"""
        subtotal = base_price * duration_days
        discount_rate = self._get_discount_rate(duration_days)
        discount = subtotal * discount_rate
        total = subtotal - discount
        
        return {
            'strategy': 'Discount Pricing',
            'base_price': base_price,
            'duration_days': duration_days,
            'discount': discount,
            'discount_rate': f'{discount_rate * 100}%',
            'surcharge': 0,
            'total': total,
            'note': self._get_discount_message(duration_days)
        }
    
    def _get_discount_rate(self, days):
        """Get discount rate based on rental duration"""
        if days >= 30:
            return 0.20  # 20% discount for 30+ days
        elif days >= 14:
            return 0.15  # 15% discount for 14-29 days
        elif days >= 7:
            return 0.10  # 10% discount for 7-13 days
        else:
            return 0  # No discount for less than 7 days
    
    def _get_discount_message(self, days):
        """Get discount message"""
        if days >= 30:
            return '20% discount for monthly rental'
        elif days >= 14:
            return '15% discount for bi-weekly rental'
        elif days >= 7:
            return '10% discount for weekly rental'
        else:
            return 'No discount applied'
