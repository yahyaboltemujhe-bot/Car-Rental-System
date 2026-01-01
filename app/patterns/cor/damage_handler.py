from abc import ABC, abstractmethod

class DamageHandler(ABC):
    """Base handler for damage claim processing chain"""
    
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler):
        """Set the next handler in the chain"""
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def can_handle(self, claim):
        """Check if this handler can process the claim"""
        pass
    
    @abstractmethod
    def process(self, claim):
        """Process the damage claim"""
        pass
    
    def handle(self, claim):
        """Handle the claim or pass to next handler"""
        if self.can_handle(claim):
            return self.process(claim)
        elif self._next_handler:
            return self._next_handler.handle(claim)
        else:
            return {
                'status': 'rejected',
                'handler': 'None',
                'message': 'No handler available for this claim'
            }
