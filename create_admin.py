"""
Admin User Creation Script for Production

Creates default admin user for first login.
Run this in Render Shell after running init_db.py

IMPORTANT: Change the password immediately after first login!
"""

from app import create_app, db
# Adjust this import based on your actual admin model location
# from app.models import Admin  # If you have a models.py
# from app.domain.admin import Admin  # If admin is in domain layer

def create_admin_user():
    """Create default admin user"""
    app = create_app()
    
    with app.app_context():
        # Uncomment and modify based on your Admin model
        
        # Example for Flask-Login User model
        '''
        admin = Admin.query.filter_by(username='admin').first()
        
        if not admin:
            admin = Admin(
                username='admin',
                email='admin@carrental.com'
            )
            admin.set_password('admin123')  # Change this password!
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully!")
            print("📧 Email: admin@carrental.com")
            print("👤 Username: admin")
            print("🔑 Password: admin123")
            print("\n⚠️  IMPORTANT: Change this password immediately after first login!")
        else:
            print("ℹ️  Admin user already exists")
        '''
        
        print("⚠️  Please uncomment and modify this script based on your Admin model")
        print("📝 Update the import statement and Admin creation code")

if __name__ == "__main__":
    create_admin_user()
