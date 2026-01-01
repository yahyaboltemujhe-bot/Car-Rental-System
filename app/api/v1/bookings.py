"""
REST API endpoints for booking operations
"""
from flask import Blueprint, jsonify, request, current_app
from app.services.booking_service import BookingService
from app.utils.exceptions import BookingNotFoundException, InvalidBookingDatesException
from datetime import datetime

api_bookings_bp = Blueprint('api_bookings', __name__, url_prefix='/api/v1/bookings')
booking_service = BookingService()


@api_bookings_bp.route('/', methods=['POST'])
def create_booking():
    """
    Create a new booking
    
    Request Body (JSON):
        {
            "car_id": int,
            "customer_name": str,
            "customer_phone": str,
            "customer_cnic": str,
            "start_date": str (YYYY-MM-DD),
            "end_date": str (YYYY-MM-DD),
            "pricing_strategy": str (optional, default: "base")
        }
    
    Returns:
        JSON object with booking details and access code
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['car_id', 'customer_name', 'customer_phone', 'customer_cnic', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Parse dates
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
        
        # Create booking
        result = booking_service.create_booking(
            car_id=data['car_id'],
            customer_name=data['customer_name'],
            customer_phone=data['customer_phone'],
            customer_cnic=data['customer_cnic'],
            start_date=start_date,
            end_date=end_date,
            pricing_strategy=data.get('pricing_strategy', 'base')
        )
        
        if result['success']:
            booking = result['booking']
            return jsonify({
                'success': True,
                'data': {
                    'booking_id': booking.id,
                    'access_code': result['access_code'],
                    'car_id': booking.car_id,
                    'customer_name': booking.customer_name,
                    'start_date': booking.start_date.strftime('%Y-%m-%d'),
                    'end_date': booking.end_date.strftime('%Y-%m-%d'),
                    'total_amount': booking.total_amount,
                    'status': booking.status,
                    'pricing_details': result['price_info']
                }
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': result['message']
            }), 400
            
    except Exception as e:
        current_app.logger.error(f'API Booking Error: {str(e)}')
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@api_bookings_bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """
    Get booking details by ID
    
    Query Parameters:
        - access_code: Required for security verification
    
    Returns:
        JSON object with booking details
    """
    try:
        from app.data.booking_repository import BookingRepository
        
        booking = BookingRepository.get_by_id(booking_id)
        
        if not booking:
            return jsonify({
                'success': False,
                'error': 'Booking not found'
            }), 404
        
        # Verify access code if provided
        access_code = request.args.get('access_code')
        if access_code and booking.access_code != access_code:
            return jsonify({
                'success': False,
                'error': 'Invalid access code'
            }), 403
        
        booking_data = {
            'booking_id': booking.id,
            'car_id': booking.car_id,
            'customer_name': booking.customer_name,
            'customer_phone': booking.customer_phone,
            'start_date': booking.start_date.strftime('%Y-%m-%d'),
            'end_date': booking.end_date.strftime('%Y-%m-%d'),
            'total_amount': booking.total_amount,
            'status': booking.status,
            'created_at': booking.created_at.isoformat() if booking.created_at else None
        }
        
        # Only include access code if verified
        if access_code and booking.access_code == access_code:
            booking_data['access_code'] = booking.access_code
        
        return jsonify({
            'success': True,
            'data': booking_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'API Error: {str(e)}')
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@api_bookings_bp.route('/verify', methods=['POST'])
def verify_booking():
    """
    Verify booking with access code
    
    Request Body (JSON):
        {
            "booking_id": int,
            "access_code": str
        }
    
    Returns:
        JSON object with verification result
    """
    try:
        from app.data.booking_repository import BookingRepository
        
        data = request.get_json()
        
        if 'booking_id' not in data or 'access_code' not in data:
            return jsonify({
                'success': False,
                'error': 'booking_id and access_code required'
            }), 400
        
        is_valid = BookingRepository.verify_access_code(
            data['booking_id'],
            data['access_code']
        )
        
        return jsonify({
            'success': True,
            'verified': is_valid
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'API Error: {str(e)}')
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
