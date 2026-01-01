from .damage_handler import DamageHandler

class MinorDamageHandler(DamageHandler):
    """Handles minor damage claims (cost < $500)"""
    
    MAX_COST = 500
    
    def can_handle(self, claim):
        """Check if damage is minor"""
        estimated_cost = claim.get('estimated_cost', 0)
        return estimated_cost < self.MAX_COST
    
    def process(self, claim):
        """Process minor damage claim"""
        print(f"Minor Damage Handler processing claim for ${claim.get('estimated_cost')}")
        
        # Minor damages are auto-approved
        return {
            'status': 'approved',
            'handler': 'MinorDamageHandler',
            'estimated_cost': claim.get('estimated_cost'),
            'message': f"Minor damage claim approved. Cost: ${claim.get('estimated_cost')}",
            'action': 'Schedule repair at local shop'
        }
