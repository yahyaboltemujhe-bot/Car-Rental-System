from flask import Blueprint, redirect, url_for, flash
from flask_login import logout_user, login_required

logout_bp = Blueprint('logout', __name__, url_prefix='/auth')

@logout_bp.route('/logout')
@login_required
def logout():
    """Handle admin logout"""
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login.login'))
