from .damage_handler import DamageHandler

class MajorDamageHandler(DamageHandler):
    """Handles major damage claims ($500 - $3000)"""
    
    MIN_COST = 500
    MAX_COST = 3000
    
    def can_handle(self, claim):
        """Check if damage is major but not insurance-level"""
        estimated_cost = claim.get('estimated_cost', 0)
        return self.MIN_COST <= estimated_cost < self.MAX_COST
    
    def process(self, claim):
        """Process major damage claim"""
        print(f"Major Damage Handler processing claim for ${claim.get('estimated_cost')}")
        
        # Major damages require admin approval
        return {
            'status': 'pending_approval',
            'handler': 'MajorDamageHandler',
            'estimated_cost': claim.get('estimated_cost'),
            'message': f"Major damage claim requires admin approval. Cost: ${claim.get('estimated_cost')}",
            'action': 'Get detailed inspection and admin approval'
        }
