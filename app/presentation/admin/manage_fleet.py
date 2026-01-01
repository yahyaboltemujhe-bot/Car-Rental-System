from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required
from app.services.fleet_service import FleetService

manage_fleet_bp = Blueprint('manage_fleet', __name__, url_prefix='/admin')
fleet_service = FleetService()

@manage_fleet_bp.route('/fleet')
@login_required
def fleet():
    """Display all vehicles in fleet with statistics"""
    cars = fleet_service.get_all_cars()
    stats = fleet_service.get_fleet_statistics()
    return render_template('admin/manage_fleet.html', cars=cars, stats=stats)

@manage_fleet_bp.route('/fleet/update-status/<int:car_id>', methods=['POST'])
@login_required
def update_status(car_id):
    """Update car status using State pattern"""
    new_status = request.form.get('status')
    car = fleet_service.update_car_status(car_id, new_status)
    
    if car:
        return jsonify({'success': True, 'status': car.status})
    return jsonify({'success': False}), 404
