from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.booking_service import BookingService
from app.services.fleet_service import FleetService
from datetime import datetime, timedelta

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')
booking_service = BookingService()
fleet_service = FleetService()

@booking_bp.route('/book/<int:car_id>')
def book_car_form(car_id):
    """Show booking form for a specific car"""
    car = fleet_service.get_car_by_id(car_id)
    
    if not car:
        flash('Car not found', 'error')
        return redirect(url_for('customer.browse_cars'))
    
    if car.status != 'available':
        flash('This car is not available for booking', 'error')
        return redirect(url_for('customer.browse_cars'))
    
    # Set default dates (today + 1 day for start, +3 days for end)
    default_start = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    default_end = (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')
    
    return render_template('customer/book_car.html',
                         car=car,
                         default_start=default_start,
                         default_end=default_end)

@booking_bp.route('/submit', methods=['POST'])
def submit_booking():
    """Process booking form submission"""
    try:
        # Get form data
        car_id = int(request.form.get('car_id'))
        customer_name = request.form.get('customer_name').strip()
        customer_phone = request.form.get('customer_phone').strip()
        customer_cnic = request.form.get('customer_cnic').strip()
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        pricing_strategy = request.form.get('pricing_strategy', 'base')
        
        # Validate inputs
        if not all([customer_name, customer_phone, customer_cnic, start_date_str, end_date_str]):
            flash('All fields are required', 'error')
            return redirect(url_for('booking.book_car_form', car_id=car_id))
        
        # Parse dates
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        
        # Validate dates
        if start_date < datetime.now():
            flash('Start date cannot be in the past', 'error')
            return redirect(url_for('booking.book_car_form', car_id=car_id))
        
        if end_date <= start_date:
            flash('End date must be after start date', 'error')
            return redirect(url_for('booking.book_car_form', car_id=car_id))
        
        # Create booking
        result = booking_service.create_booking(
            car_id=car_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_cnic=customer_cnic,
            start_date=start_date,
            end_date=end_date,
            pricing_strategy=pricing_strategy
        )
        
        if result['success']:
            # Store booking info in session for confirmation page
            session['booking_id'] = result['booking'].id
            session['access_code'] = result['access_code']
            
            flash('Booking created successfully!', 'success')
            return redirect(url_for('booking.booking_confirmation', booking_id=result['booking'].id))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('booking.book_car_form', car_id=car_id))
            
    except ValueError as e:
        flash(f'Invalid input: {str(e)}', 'error')
        return redirect(url_for('customer.browse_cars'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('customer.browse_cars'))

@booking_bp.route('/confirmation/<int:booking_id>')
def booking_confirmation(booking_id):
    """Show booking confirmation with access code"""
    from app.data.booking_repository import BookingRepository
    from app.data.car_repository import CarRepository
    
    booking = BookingRepository.get_by_id(booking_id)
    
    if not booking:
        flash('Booking not found', 'error')
        return redirect(url_for('customer.browse_cars'))
    
    car = CarRepository.get_by_id(booking.car_id)
    
    # Get access code from session if available
    access_code = session.get('access_code', 'N/A')
    
    # Calculate rental details
    duration_days = (booking.end_date - booking.start_date).days
    
    return render_template('customer/booking_confirmation.html',
                         booking=booking,
                         car=car,
                         access_code=access_code,
                         duration_days=duration_days)

@booking_bp.route('/lookup')
def lookup_form():
    """Show form to lookup booking by ID and phone"""
    return render_template('customer/lookup_booking.html')

@booking_bp.route('/lookup/search', methods=['POST'])
def lookup_search():
    """Search for booking"""
    from app.data.booking_repository import BookingRepository
    from app.data.car_repository import CarRepository
    
    booking_id = request.form.get('booking_id')
    customer_phone = request.form.get('customer_phone')
    
    if not booking_id or not customer_phone:
        flash('Please provide both Booking ID and phone number', 'error')
        return redirect(url_for('booking.lookup_form'))
    
    try:
        booking = BookingRepository.get_by_id(int(booking_id))
        
        if not booking:
            flash('Booking not found', 'error')
            return redirect(url_for('booking.lookup_form'))
        
        # Verify phone number matches
        if booking.customer_phone != customer_phone:
            flash('Phone number does not match booking records', 'error')
            return redirect(url_for('booking.lookup_form'))
        
        car = CarRepository.get_by_id(booking.car_id)
        duration_days = (booking.end_date - booking.start_date).days
        
        return render_template('customer/booking_details.html',
                             booking=booking,
                             car=car,
                             duration_days=duration_days)
        
    except ValueError:
        flash('Invalid booking ID', 'error')
        return redirect(url_for('booking.lookup_form'))
