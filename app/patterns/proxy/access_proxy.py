from .car_access import CarAccess
from datetime import datetime

class AccessProxy:
    """Proxy for car access - adds security verification layer (Keyless Entry System)"""
    
    def __init__(self, car_id, required_access_code):
        self.car_id = car_id
        self.required_access_code = required_access_code
        self._real_access = CarAccess(car_id)
        self.access_attempts = []
        self.is_authenticated = False
    
    def verify_access(self, provided_code):
        """Verify access code before granting access"""
        attempt = {
            'timestamp': datetime.now(),
            'success': False,
            'code_provided': provided_code
        }
        
        if provided_code == self.required_access_code:
            self.is_authenticated = True
            attempt['success'] = True
            print(f"✅ Keyless Access GRANTED for car {self.car_id}")
        else:
            print(f"❌ Keyless Access DENIED for car {self.car_id} - Invalid code")
        
        self.access_attempts.append(attempt)
        return attempt['success']
    
    def unlock(self, access_code):
        """Unlock car after verifying access code (Keyless Entry)"""
        if self.verify_access(access_code):
            return self._real_access.unlock()
        else:
            return {
                'success': False,
                'message': 'Access denied - Invalid access code'
            }
    
    def lock(self):
        """Lock the car (no authentication needed)"""
        if self.is_authenticated:
            return self._real_access.lock()
        else:
            return {
                'success': False,
                'message': 'Authentication required'
            }
    
    def start_engine(self, access_code):
        """Start engine with keyless entry (Proxy Pattern)"""
        if self.verify_access(access_code):
            return self._real_access.start_engine()
        else:
            return {
                'success': False,
                'message': 'Access denied - Cannot start engine'
            }
    
    def get_car_status(self, access_code):
        """Get car status (locked/unlocked, engine state)"""
        if self.verify_access(access_code):
            return {
                'success': True,
                'car_id': self.car_id,
                'is_unlocked': self._real_access.is_unlocked,
                'engine_running': self._real_access.engine_running,
                'last_access': self._real_access.last_access.isoformat() if self._real_access.last_access else None
            }
        else:
            return {
                'success': False,
                'message': 'Access denied'
            }
    
    def get_access_log(self):
        """Get access attempt history (for admin monitoring)"""
        return {
            'car_id': self.car_id,
            'total_attempts': len(self.access_attempts),
            'successful_attempts': sum(1 for a in self.access_attempts if a['success']),
            'failed_attempts': sum(1 for a in self.access_attempts if not a['success']),
            'attempts': self.access_attempts
        }
        if self.is_authenticated:
            return self._real_access.lock()
        else:
            print("Lock failed - Not authenticated")
            return False
    
    def start_engine(self, access_code):
        """Start engine after verification"""
        if not self.is_authenticated:
            if not self.verify_access(access_code):
                print("Cannot start engine - Authentication failed")
                return False
        
        return self._real_access.start_engine()
    
    def get_status(self):
        """Get access status with authentication info"""
        status = self._real_access.get_status()
        status['is_authenticated'] = self.is_authenticated
        status['access_attempts'] = len(self.access_attempts)
        status['failed_attempts'] = len([a for a in self.access_attempts if not a['success']])
        return status
    
    def revoke_access(self):
        """Revoke authentication"""
        self.is_authenticated = False
        self._real_access.lock()
        print(f"Access revoked for car {self.car_id}")
