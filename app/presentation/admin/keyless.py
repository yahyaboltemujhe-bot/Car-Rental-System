from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required
from app.services.booking_service import BookingService
from app.data.car_repository import CarRepository
from app.patterns.proxy.access_proxy import AccessProxy

keyless_bp = Blueprint('keyless', __name__, url_prefix='/admin')
booking_service = BookingService()

@keyless_bp.route('/keyless')
@login_required
def keyless_entry():
    """Keyless entry system demonstrating Proxy Pattern"""
    active_bookings = booking_service.get_active_bookings()
    return render_template('admin/keyless.html', bookings=active_bookings)

@keyless_bp.route('/keyless/verify', methods=['POST'])
@login_required
def verify_code():
    """Verify access code and return car details"""
    access_code = request.json.get('access_code')
    
    booking = booking_service.verify_access_code(access_code)
    
    if booking:
        # Reset car status if it's out of range (for keyless demo purposes)
        if booking.car.status == 'out_of_range':
            CarRepository.update_status(booking.car_id, 'booked')
            
        return jsonify({
            'success': True,
            'booking_id': booking.id,
            'car_id': booking.car_id,
            'car_model': booking.car.model,
            'license_plate': booking.car.license_plate,
            'customer_name': booking.customer_name,
            'access_code': booking.access_code
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid access code'
        }), 401

@keyless_bp.route('/keyless/unlock', methods=['POST'])
@login_required
def unlock_car():
    """Unlock car using Proxy Pattern"""
    data = request.json
    car_id = data.get('car_id')
    access_code = data.get('access_code')
    
    # Create Access Proxy (Proxy Pattern)
    proxy = AccessProxy(car_id, access_code)
    
    # Attempt to unlock through proxy
    result = proxy.unlock(access_code)
    
    return jsonify(result)

@keyless_bp.route('/keyless/lock', methods=['POST'])
@login_required
def lock_car():
    """Lock car using Proxy Pattern"""
    data = request.json
    car_id = data.get('car_id')
    access_code = data.get('access_code')
    
    proxy = AccessProxy(car_id, access_code)
    # Authenticate and lock
    if proxy.verify_access(access_code):
        result = proxy._real_access.lock()
        return jsonify(result)
    else:
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        })

@keyless_bp.route('/keyless/start-engine', methods=['POST'])
@login_required
def start_engine():
    """Start engine using Proxy Pattern (Push-button start)"""
    data = request.json
    car_id = data.get('car_id')
    access_code = data.get('access_code')
    
    proxy = AccessProxy(car_id, access_code)
    
    # First verify and unlock if needed
    if proxy.verify_access(access_code):
        # Unlock first (in case it's locked)
        unlock_result = proxy._real_access.unlock()
        
        # Then start engine
        result = proxy._real_access.start_engine()
        return jsonify(result)
    else:
        return jsonify({
            'success': False,
            'message': 'Access denied - Cannot start engine'
        })

@keyless_bp.route('/keyless/status', methods=['POST'])
@login_required
def get_status():
    """Get car status through Proxy"""
    data = request.json
    car_id = data.get('car_id')
    access_code = data.get('access_code')
    
    proxy = AccessProxy(car_id, access_code)
    result = proxy.get_car_status(access_code)
    
    return jsonify(result)

@keyless_bp.route('/keyless/reset-location/<int:car_id>', methods=['POST'])
@login_required
def reset_location(car_id):
    """Reset car to rental location (for testing purposes)"""
    car = CarRepository.get_by_id(car_id)
    
    if car and car.rental_location_lat and car.rental_location_lng:
        # Reset to rental location
        CarRepository.update_location(car_id, car.rental_location_lat, car.rental_location_lng)
        
        # Update status if out of range
        if car.status == 'out_of_range':
            CarRepository.update_status(car_id, 'booked')
        
        return jsonify({
            'success': True,
            'message': f'Car {car.license_plate} location reset to rental point'
        })
    
    return jsonify({
        'success': False,
        'message': 'Car not found or rental location not set'
    }), 404

@keyless_bp.route('/keyless/access-log/<int:car_id>')
@login_required
def access_log(car_id):
    """View access attempt log for a car"""
    # This would typically store logs in database
    # For demo, we'll show the concept
    return jsonify({
        'car_id': car_id,
        'message': 'Access logs stored securely via Proxy Pattern'
    })
