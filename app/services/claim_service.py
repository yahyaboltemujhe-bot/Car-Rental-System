from app.data.claim_repository import ClaimRepository
from app.data.car_repository import CarRepository
from app.patterns.cor.minor_damage import MinorDamageHandler
from app.patterns.cor.major_damage import MajorDamageHandler
from app.patterns.cor.insurance_handler import InsuranceHandler
from app.patterns.observer.subject import Subject

class ClaimService:
    """Service for processing damage claims using Chain of Responsibility"""
    
    def __init__(self):
        self.notification_system = Subject()
        
        # Set up the chain of responsibility
        self.minor_handler = MinorDamageHandler()
        self.major_handler = MajorDamageHandler()
        self.insurance_handler = InsuranceHandler()
        
        # Chain: Minor -> Major -> Insurance
        self.minor_handler.set_next(self.major_handler)
        self.major_handler.set_next(self.insurance_handler)
    
    def file_claim(self, car_id, booking_id, damage_type, description, estimated_cost):
        """File a new damage claim"""
        car = CarRepository.get_by_id(car_id)
        if not car:
            return {'success': False, 'message': 'Car not found'}
        
        # Create the claim
        claim = ClaimRepository.create(
            car_id=car_id,
            booking_id=booking_id,
            damage_type=damage_type,
            description=description,
            estimated_cost=estimated_cost
        )
        
        # Process through chain of responsibility
        claim_data = {
            'id': claim.id,
            'car_id': car_id,
            'estimated_cost': estimated_cost,
            'damage_type': damage_type,
            'description': description
        }
        
        result = self.minor_handler.handle(claim_data)
        
        # Update claim with processing result
        ClaimRepository.update_status(
            claim.id,
            result['status'],
            result['handler']
        )
        
        # Notify observers
        self.notification_system.notify('damage_claim_filed', {
            'claim_id': claim.id,
            'car_id': car_id,
            'license_plate': car.license_plate,
            'estimated_cost': estimated_cost,
            'status': result['status']
        })
        
        return {
            'success': True,
            'claim': claim,
            'processing_result': result
        }
    
    def get_all_claims(self):
        """Get all claims"""
        return ClaimRepository.get_all()
    
    def get_pending_claims(self):
        """Get pending claims"""
        return ClaimRepository.get_pending_claims()
    
    def get_claims_by_car(self, car_id):
        """Get all claims for a specific car"""
        return ClaimRepository.get_by_car(car_id)
    
    def approve_claim(self, claim_id):
        """Approve a claim"""
        return ClaimRepository.update_status(claim_id, 'approved')
    
    def reject_claim(self, claim_id):
        """Reject a claim"""
        return ClaimRepository.update_status(claim_id, 'rejected')
