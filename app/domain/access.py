from datetime import datetime

class Access:
    """Access domain entity for car access verification"""
    
    def __init__(self, car_id, access_code, booking_id):
        self.car_id = car_id
        self.access_code = access_code
        self.booking_id = booking_id
        self.is_valid = True
        self.last_verified = None
    
    def verify(self, provided_code):
        """Verify the access code"""
        if not self.is_valid:
            return False
        
        if self.access_code == provided_code:
            self.last_verified = datetime.now()
            return True
        
        return False
    
    def revoke(self):
        """Revoke access"""
        self.is_valid = False
    
    def grant(self):
        """Grant access"""
        self.is_valid = True
    
    def __repr__(self):
        status = 'Valid' if self.is_valid else 'Revoked'
        return f'<Access Car:{self.car_id} - {status}>'
