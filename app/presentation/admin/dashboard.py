from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.fleet_service import FleetService
from app.services.booking_service import BookingService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
fleet_service = FleetService()
booking_service = BookingService()

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard showing fleet and booking statistics"""
    stats = fleet_service.get_fleet_statistics()
    active_bookings = booking_service.get_active_bookings()
    return render_template('admin/dashboard_enhanced.html', 
                         stats=stats, 
                         active_bookings=active_bookings,
                         current_user=current_user)
