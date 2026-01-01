from flask import session

class AdminNotifier:
    """Observer that sends notifications to admin dashboard and UI"""
    
    def __init__(self):
        self.notifications = []
    
    def update(self, event_type, data):
        """Receive notification and store it, also trigger UI notification"""
        notification = {
            'type': event_type,
            'message': self._format_message(event_type, data),
            'data': data
        }
        self.notifications.append(notification)
        print(f"[ADMIN NOTIFICATION] {notification['message']}")
        
        # Store in session for UI toast notification (Observer Pattern)
        self._store_notification_for_ui(event_type, notification['message'])
    
    def _format_message(self, event_type, data):
        """Format notification message based on event type"""
        if event_type == 'car_out_of_range':
            model = data.get('model', 'Unknown Model')
            plate = data.get('license_plate', 'Unknown')
            distance = data.get('distance', 0)
            max_allowed = data.get('max_allowed', 0)
            tracker = data.get('tracker_type', 'GPS')
            current_loc = data.get('current_location', (0, 0))
            
            return (f"🚨 VEHICLE OUT OF RANGE! {model} ({plate}) has moved {distance:.2f} km "
                   f"from rental location (Max: {max_allowed} km). "
                   f"Tracked via {tracker} at {current_loc[0]:.4f}, {current_loc[1]:.4f}")
        
        elif event_type == 'car_returned_to_range':
            model = data.get('model', 'Unknown Model')
            plate = data.get('license_plate', 'Unknown')
            return f"✅ {model} ({plate}) has returned to the allowed zone"
        
        messages = {
            'car_booked': f"Car {data.get('license_plate')} has been booked",
            'booking_completed': f"Booking {data.get('booking_id')} completed",
            'damage_claim_filed': f"New damage claim filed for car {data.get('license_plate')}",
            'car_returned': f"Car {data.get('license_plate')} has been returned",
            'maintenance_required': f"Car {data.get('license_plate')} requires maintenance"
        }
        return messages.get(event_type, f"Event: {event_type}")
    
    def _store_notification_for_ui(self, event_type, message):
        """Store notification in session for UI toast display"""
        try:
            session['pending_notification'] = {
                'type': event_type,
                'message': message
            }
        except RuntimeError:
            # Session not available (e.g., outside request context)
            pass
    
    def get_recent_notifications(self, limit=10):
        """Get recent notifications"""
        return self.notifications[-limit:]
    
    def clear_notifications(self):
        """Clear all notifications"""
        self.notifications = []
