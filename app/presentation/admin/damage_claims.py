from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.claim_service import ClaimService
from app.services.fleet_service import FleetService

damage_claims_bp = Blueprint('damage_claims', __name__, url_prefix='/admin')
claim_service = ClaimService()
fleet_service = FleetService()

@damage_claims_bp.route('/claims')
@login_required
def claims():
    """Display all damage claims processed via Chain of Responsibility"""
    all_claims = claim_service.get_all_claims()
    pending_claims = claim_service.get_pending_claims()
    cars = fleet_service.get_all_cars()  # Add cars for modal dropdown
    return render_template('admin/damage_claims.html', claims=all_claims, pending=pending_claims, cars=cars)

@damage_claims_bp.route('/claims/file', methods=['GET', 'POST'])
@login_required
def file_claim():
    """File new damage claim - processed through CoR chain"""
    if request.method == 'POST':
        car_id = request.form.get('car_id')
        booking_id = request.form.get('booking_id')
        damage_type = request.form.get('damage_type')
        description = request.form.get('description')
        estimated_cost = request.form.get('estimated_cost')
        
        # Validate
        if not car_id or not damage_type or not description or not estimated_cost:
            flash('All required fields must be filled', 'error')
            return redirect(url_for('damage_claims.claims'))
        
        try:
            result = claim_service.file_claim(
                car_id=int(car_id),
                booking_id=int(booking_id) if booking_id else None,
                damage_type=damage_type,
                description=description,
                estimated_cost=float(estimated_cost)
            )
            
            if result['success']:
                processing_result = result['processing_result']
                flash(f"Claim filed! {processing_result['message']}", 'success')
            else:
                flash(result.get('message', 'Failed to file claim'), 'error')
        except Exception as e:
            flash(f'Error filing claim: {str(e)}', 'error')
        
        return redirect(url_for('damage_claims.claims'))
    
    cars = fleet_service.get_all_cars()
    return render_template('admin/file_claim.html', cars=cars)

@damage_claims_bp.route('/claims/approve/<int:claim_id>', methods=['POST'])
@login_required
def approve_claim(claim_id):
    """Approve a pending claim"""
    claim_service.approve_claim(claim_id)
    flash('Claim approved successfully', 'success')
    return redirect(url_for('damage_claims.claims'))

@damage_claims_bp.route('/claims/reject/<int:claim_id>', methods=['POST'])
@login_required
def reject_claim(claim_id):
    """Reject a pending claim"""
    claim_service.reject_claim(claim_id)
    flash('Claim rejected', 'info')
    return redirect(url_for('damage_claims.claims'))
