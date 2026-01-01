from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from app.models import Admin

login_bp = Blueprint('login', __name__, url_prefix='/auth')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    """Handle admin login"""
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate input
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('auth/login.html')
        
        # Find admin user
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            flash(f'Welcome back, {admin.username}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')
