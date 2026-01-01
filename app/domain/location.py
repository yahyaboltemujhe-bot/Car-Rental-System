from datetime import datetime

class Location:
    """Location domain entity for GPS tracking"""
    
    def __init__(self, car_id, latitude, longitude):
        self.car_id = car_id
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = datetime.now()
        self.is_out_of_range = False
    
    def get_coordinates(self):
        """Get location coordinates as tuple"""
        return (self.latitude, self.longitude)
    
    def mark_out_of_range(self):
        """Mark this location as out of allowed range"""
        self.is_out_of_range = True
    
    def mark_in_range(self):
        """Mark this location as within allowed range"""
        self.is_out_of_range = False
    
    def __repr__(self):
        range_status = 'OUT OF RANGE' if self.is_out_of_range else 'In Range'
        return f'<Location Car:{self.car_id} ({self.latitude}, {self.longitude}) - {range_status}>'
