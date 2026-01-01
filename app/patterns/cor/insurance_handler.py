from .damage_handler import DamageHandler

class InsuranceHandler(DamageHandler):
    """Handles severe damage claims requiring insurance (>= $3000)"""
    
    MIN_COST = 3000
    
    def can_handle(self, claim):
        """Check if damage requires insurance"""
        estimated_cost = claim.get('estimated_cost', 0)
        return estimated_cost >= self.MIN_COST
    
    def process(self, claim):
        """Process insurance-level damage claim"""
        print(f"Insurance Handler processing claim for ${claim.get('estimated_cost')}")
        
        # Severe damages go to insurance
        return {
            'status': 'insurance_claim',
            'handler': 'InsuranceHandler',
            'estimated_cost': claim.get('estimated_cost'),
            'message': f"Severe damage - Insurance claim required. Cost: ${claim.get('estimated_cost')}",
            'action': 'File insurance claim and contact insurance company'
        }
