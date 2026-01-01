from datetime import datetime
import os

class AlertLogger:
    """Observer that logs all system alerts to a file"""
    
    def __init__(self, log_file='logs/alerts.log'):
        self.log_file = log_file
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Create logs directory if it doesn't exist"""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def update(self, event_type, data):
        """Log the event to file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {event_type.upper()}: {data}\n"
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
            print(f"[ALERT LOGGED] {event_type}")
        except Exception as e:
            print(f"Error logging alert: {e}")
    
    def get_logs(self, lines=50):
        """Get recent log entries"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    all_lines = f.readlines()
                    return all_lines[-lines:]
        except Exception as e:
            print(f"Error reading logs: {e}")
        return []
