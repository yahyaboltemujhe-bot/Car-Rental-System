from flask import Blueprint, render_template, request, jsonify
from app.services.fleet_service import FleetService

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')
fleet_service = FleetService()

@customer_bp.route('/')
@customer_bp.route('/browse')
def browse_cars():
    """Browse available cars for rent"""
    # Get filter parameters
    category = request.args.get('category', 'all')
    
    # Get all cars - use get_available_cars() directly for better performance
    if category == 'all':
        available_cars = fleet_service.get_available_cars()
    else:
        # Get all available cars and filter by category
        all_available = fleet_service.get_available_cars()
        available_cars = [car for car in all_available if car.category.lower() == category.lower()]
    
    # Get statistics
    stats = {
        'total_available': len(available_cars),
        'economy': sum(1 for car in available_cars if car.category.lower() == 'economy'),
        'luxury': sum(1 for car in available_cars if car.category.lower() == 'luxury'),
        'suv': sum(1 for car in available_cars if car.category.lower() == 'suv')
    }
    
    return render_template('customer/browse_cars.html',
                         cars=available_cars,
                         stats=stats,
                         selected_category=category)
