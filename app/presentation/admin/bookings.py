"""
Admin Booking Management Routes
Admin can manually create, view, and manage customer bookings
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.services.booking_service import BookingService
from app.services.fleet_service import FleetService
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)
booking_service = BookingService()
fleet_service = FleetService()

@bookings_bp.route('/admin/bookings')
@login_required
def list_bookings():
    """List all bookings"""
    bookings = booking_service.get_all_bookings()
    return render_template('admin/bookings.html', bookings=bookings)

@bookings_bp.route('/admin/bookings/create', methods=['GET', 'POST'])
@login_required
def create_booking():
    """Admin creates a new booking manually"""
    if request.method == 'POST':
        try:
            # Extract form data
            car_id = int(request.form.get('car_id'))
            customer_name = request.form.get('customer_name')
            customer_phone = request.form.get('customer_phone')
            customer_cnic = request.form.get('customer_cnic')
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
            pricing_strategy = request.form.get('pricing_strategy', 'base')
            
            # Create booking using Strategy pattern for pricing
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
                flash(f"Booking created successfully! Access Code: {result['booking'].access_code}", 'success')
                return redirect(url_for('bookings.list_bookings'))
            else:
                flash(result.get('message', 'Failed to create booking'), 'error')
        except Exception as e:
            flash(f'Error creating booking: {str(e)}', 'error')
    
    # GET request - show form
    available_cars = fleet_service.get_available_cars()
    return render_template('admin/create_booking.html', cars=available_cars)

@bookings_bp.route('/admin/bookings/<int:booking_id>')
@login_required
def view_booking(booking_id):
    """View booking details"""
    booking = booking_service.get_booking_by_id(booking_id)
    if not booking:
        flash('Booking not found', 'error')
        return redirect(url_for('bookings.list_bookings'))
    return render_template('admin/booking_details.html', booking=booking)

@bookings_bp.route('/admin/bookings/<int:booking_id>/complete', methods=['POST'])
@login_required
def complete_booking(booking_id):
    """Mark booking as completed"""
    try:
        booking_service.complete_booking(booking_id)
        flash('Booking completed successfully', 'success')
    except Exception as e:
        flash(f'Error completing booking: {str(e)}', 'error')
    return redirect(url_for('bookings.list_bookings'))

@bookings_bp.route('/admin/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking"""
    try:
        booking_service.cancel_booking(booking_id)
        flash('Booking cancelled successfully', 'success')
    except Exception as e:
        flash(f'Error cancelling booking: {str(e)}', 'error')
    return redirect(url_for('bookings.list_bookings'))

@bookings_bp.route('/admin/bookings/verify', methods=['POST'])
@login_required
def verify_access():
    """Verify customer access code"""
    access_code = request.form.get('access_code')
    booking = booking_service.verify_access_code(access_code)
    
    if booking:
        return jsonify({
            'success': True,
            'booking_id': booking.id,
            'customer_name': booking.customer_name,
            'car': booking.car.model,
            'status': booking.status
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid access code'
        }), 404
