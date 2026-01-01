from datetime import datetime

class CarAccess:
    """Real subject for car access - handles actual car operations (Keyless System)"""
    
    def __init__(self, car_id):
        self.car_id = car_id
        self.is_unlocked = False
        self.engine_running = False
        self.last_access = None
    
    def unlock(self):
        """Unlock the car (Keyless Entry)"""
        self.is_unlocked = True
        self.last_access = datetime.now()
        print(f"🔓 Car {self.car_id} UNLOCKED (Keyless Entry)")
        return {
            'success': True,
            'message': f'Car {self.car_id} unlocked successfully',
            'is_unlocked': True
        }
    
    def lock(self):
        """Lock the car"""
        self.is_unlocked = False
        self.engine_running = False
        print(f"🔒 Car {self.car_id} LOCKED")
        return {
            'success': True,
            'message': f'Car {self.car_id} locked successfully',
            'is_unlocked': False
        }
    
    def start_engine(self):
        """Start the car engine (Push-button start)"""
        if self.is_unlocked:
            self.engine_running = True
            print(f"🚗 Car {self.car_id} engine STARTED (Push-button start)")
            return {
                'success': True,
                'message': 'Engine started successfully',
                'engine_running': True
            }
        else:
            print(f"❌ Cannot start engine - Car {self.car_id} is locked")
            return {
                'success': False,
                'message': 'Cannot start engine - Car is locked'
            }
    
    def stop_engine(self):
        """Stop the car engine"""
        self.engine_running = False
        print(f"⏹️ Car {self.car_id} engine STOPPED")
        return {
            'success': True,
            'message': 'Engine stopped',
            'engine_running': False
        }
    
    def get_status(self):
        """Get current access status"""
        return {
            'car_id': self.car_id,
            'is_unlocked': self.is_unlocked,
            'engine_running': self.engine_running,
            'last_access': self.last_access.isoformat() if self.last_access else None
        }

