"""
REST API endpoints for car operations
Provides JSON API for mobile apps and third-party integrations
"""
from flask import Blueprint, jsonify, request, current_app
from app.services.fleet_service import FleetService
from app.utils.exceptions import CarNotFoundException, ValidationException
from functools import wraps

api_cars_bp = Blueprint('api_cars', __name__, url_prefix='/api/v1/cars')
fleet_service = FleetService()


def api_key_required(f):
    """Decorator to require API key for protected endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        # In production, validate against stored API keys
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        return f(*args, **kwargs)
    return decorated_function


@api_cars_bp.route('/', methods=['GET'])
def get_all_cars():
    """
    Get all cars in the fleet
    
    Query Parameters:
        - status: Filter by status (available, booked, maintenance, etc.)
        - category: Filter by category (economy, luxury, suv)
        - limit: Maximum number of results (default: 50)
        - offset: Pagination offset (default: 0)
    
    Returns:
        JSON array of car objects
    """
    try:
        status = request.args.get('status')
        category = request.args.get('category')
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        current_app.logger.info(f'API: Fetching cars (status={status}, category={category})')
        
        # Get cars based on filters
        if status:
            cars = fleet_service.get_cars_by_status(status)
        else:
            cars = fleet_service.get_all_cars()
        
        # Filter by category if specified
        if category:
            cars = [c for c in cars if c.category.lower() == category.lower()]
        
        # Apply pagination
        total = len(cars)
        cars = cars[offset:offset + limit]
        
        # Convert to dict
        cars_data = [{
            'id': car.id,
            'license_plate': car.license_plate,
            'model': car.model,
            'category': car.category,
            'status': car.status,
            'price_tier': car.price_tier,
            'daily_rate': car.price_tier * 50,
            'location': {
                'latitude': car.rental_location_lat,
                'longitude': car.rental_location_lng
            } if car.rental_location_lat else None
        } for car in cars]
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': cars_data
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'error': 'Invalid query parameters'}), 400
    except Exception as e:
        current_app.logger.error(f'API Error: {str(e)}')
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@api_cars_bp.route('/<int:car_id>', methods=['GET'])
def get_car(car_id):
    """
    Get a specific car by ID
    
    Args:
        car_id: Car ID
    
    Returns:
        JSON object with car details
    """
    try:
        car = fleet_service.get_car_by_id(car_id)
        
        if not car:
            return jsonify({
                'success': False,
                'error': 'Car not found'
            }), 404
        
        car_data = {
            'id': car.id,
            'license_plate': car.license_plate,
            'model': car.model,
            'category': car.category,
            'status': car.status,
            'price_tier': car.price_tier,
            'daily_rate': car.price_tier * 50,
            'location': {
                'current': {
                    'latitude': car.current_location_lat,
                    'longitude': car.current_location_lng
                } if car.current_location_lat else None,
                'rental': {
                    'latitude': car.rental_location_lat,
                    'longitude': car.rental_location_lng
                } if car.rental_location_lat else None
            },
            'created_at': car.created_at.isoformat() if car.created_at else None
        }
        
        return jsonify({
            'success': True,
            'data': car_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'API Error: {str(e)}')
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@api_cars_bp.route('/available', methods=['GET'])
def get_available_cars():
    """
    Get all available cars for booking
    
    Query Parameters:
        - category: Filter by category
        - min_price: Minimum daily rate
        - max_price: Maximum daily rate
    
    Returns:
        JSON array of available cars
    """
    try:
        category = request.args.get('category')
        min_price = float(request.args.get('min_price', 0))
        max_price = float(request.args.get('max_price', 10000))
        
        cars = fleet_service.get_available_cars()
        
        # Apply filters
        if category:
            cars = [c for c in cars if c.category.lower() == category.lower()]
        
        # Filter by price range
        cars = [c for c in cars if min_price <= (c.price_tier * 50) <= max_price]
        
        cars_data = [{
            'id': car.id,
            'license_plate': car.license_plate,
            'model': car.model,
            'category': car.category,
            'daily_rate': car.price_tier * 50,
            'location': {
                'latitude': car.rental_location_lat,
                'longitude': car.rental_location_lng
            } if car.rental_location_lat else None
        } for car in cars]
        
        return jsonify({
            'success': True,
            'count': len(cars_data),
            'data': cars_data
        }), 200
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid price range'}), 400
    except Exception as e:
        current_app.logger.error(f'API Error: {str(e)}')
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@api_cars_bp.route('/statistics', methods=['GET'])
@api_key_required
def get_statistics():
    """
    Get fleet statistics (requires API key)
    
    Returns:
        JSON object with fleet statistics
    """
    try:
        stats = fleet_service.get_fleet_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'API Error: {str(e)}')
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
