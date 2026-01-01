from flask import Blueprint, render_template, request, jsonify, flash, session, redirect, url_for
from flask_login import login_required
from app.services.tracking_service import TrackingService
from app.services.fleet_service import FleetService

tracking_bp = Blueprint('tracking', __name__, url_prefix='/admin')
tracking_service = TrackingService()
fleet_service = FleetService()

@tracking_bp.route('/tracking')
@login_required
def tracking():
    """Vehicle tracking with Observer pattern notifications"""
    cars = fleet_service.get_all_cars()
    out_of_range = tracking_service.get_out_of_range_cars()
    
    # Check for pending notifications from Observer pattern
    if 'pending_notification' in session:
        notification = session.pop('pending_notification')
        flash(notification['message'], notification['type'])
    
    return render_template('admin/tracking.html', cars=cars, out_of_range=out_of_range)

@tracking_bp.route('/tracking/update-location/<int:car_id>', methods=['POST'])
@login_required
def update_location(car_id):
    """Update car location and trigger Observer notifications"""
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    result = tracking_service.update_location(car_id, latitude, longitude)
    return jsonify(result)

@tracking_bp.route('/tracking/simulate-out-of-range/<int:car_id>')
@login_required
def simulate_out_of_range(car_id):
    """Simulate out-of-range notification for testing Observer pattern"""
    from app.data.car_repository import CarRepository
    
    car = CarRepository.get_by_id(car_id)
    if car:
        # Simulate location far from rental point (100 km away)
        if car.rental_location_lat and car.rental_location_lng:
            # Move car 1 degree away (approximately 111 km)
            new_lat = car.rental_location_lat + 1.0
            new_lng = car.rental_location_lng + 1.0
            
            result = tracking_service.update_location(car_id, new_lat, new_lng)
            # Don't add extra flash here, let the Observer pattern handle it
        else:
            flash('Car has no rental location set.', 'warning')
    else:
        flash('Car not found.', 'error')
    
    # Redirect to tracking page to show notification
    return redirect(url_for('tracking.tracking'))

@tracking_bp.route('/tracking/history/<int:car_id>')
@login_required
def location_history(car_id):
    """View location history for a vehicle"""
    history = tracking_service.get_location_history(car_id)
    return render_template('admin/location_history.html', history=history, car_id=car_id)
