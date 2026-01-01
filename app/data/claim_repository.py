from app.models import db, Claim
from datetime import datetime

class ClaimRepository:
    """Repository for damage claim data access"""
    
    @staticmethod
    def create(car_id, booking_id, damage_type, description, estimated_cost=None):
        """Create a new damage claim"""
        claim = Claim(
            car_id=car_id,
            booking_id=booking_id,
            damage_type=damage_type,
            description=description,
            estimated_cost=estimated_cost,
            status='pending'
        )
        db.session.add(claim)
        db.session.commit()
        return claim
    
    @staticmethod
    def get_by_id(claim_id):
        """Get claim by ID"""
        return Claim.query.get(claim_id)
    
    @staticmethod
    def get_all():
        """Get all claims"""
        return Claim.query.all()
    
    @staticmethod
    def get_pending_claims():
        """Get all pending claims"""
        return Claim.query.filter_by(status='pending').all()
    
    @staticmethod
    def get_by_car(car_id):
        """Get all claims for a specific car"""
        return Claim.query.filter_by(car_id=car_id).all()
    
    @staticmethod
    def update_status(claim_id, new_status, handler=None):
        """Update claim status"""
        claim = Claim.query.get(claim_id)
        if claim:
            claim.status = new_status
            if handler:
                claim.handler = handler
            claim.processed_at = datetime.utcnow()
            db.session.commit()
        return claim
    
    @staticmethod
    def update_cost(claim_id, estimated_cost):
        """Update estimated cost"""
        claim = Claim.query.get(claim_id)
        if claim:
            claim.estimated_cost = estimated_cost
            db.session.commit()
        return claim
