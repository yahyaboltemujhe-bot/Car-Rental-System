from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.fleet_service import FleetService

add_car_bp = Blueprint('add_car', __name__, url_prefix='/admin')
fleet_service = FleetService()

@add_car_bp.route('/add-car', methods=['GET', 'POST'])
@login_required
def add_car():
    """Add new car to fleet using Abstract Factory pattern"""
    if request.method == 'POST':
        license_plate = request.form.get('license_plate')
        model = request.form.get('model')
        category = request.form.get('category')
        rental_lat = request.form.get('rental_lat')
        rental_lng = request.form.get('rental_lng')
        
        # Validate inputs
        if not license_plate or not model or not category:
            flash('All required fields must be filled', 'error')
            return render_template('admin/add_car.html')
        
        # Convert coordinates
        try:
            rental_lat = float(rental_lat) if rental_lat else None
            rental_lng = float(rental_lng) if rental_lng else None
        except ValueError:
            flash('Invalid coordinate values', 'error')
            return render_template('admin/add_car.html')
        
        result = fleet_service.add_car(
            license_plate=license_plate,
            model=model,
            category=category,
            rental_lat=rental_lat,
            rental_lng=rental_lng
        )
        
        if result['success']:
            flash(f'Car {license_plate} added successfully to {category} fleet!', 'success')
            return redirect(url_for('manage_fleet.fleet'))
        else:
            flash(result.get('message', 'Failed to add car'), 'error')
        
    return render_template('admin/add_car.html')
