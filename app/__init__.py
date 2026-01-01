from flask import Flask, redirect, url_for, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os

def create_app():
    # Set paths relative to project root
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Load configuration
    app.config.from_object('config.Config')

    # Safety check: in production, ensure a real DATABASE_URL is provided (no SQLite fallback)
    if not app.config.get('DEBUG'):
        uri = app.config.get('SQLALCHEMY_DATABASE_URI', '') or ''
        if uri.startswith('sqlite:///') or not uri:
            msg = (
                "Missing or invalid DATABASE_URL in production. "
                "Set DATABASE_URL to your Postgres connection string in Render environment variables."
            )
            # Log and abort startup so the issue is visible in deploy logs
            app.logger.error(msg)
            raise RuntimeError(msg)
    
    # Enable CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Setup logging
    from app.utils.logger import setup_logger
    logger = setup_logger(app)
    
    # Initialize database
    from app.models import db, Admin
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))
    
    # Automatic DB initialization on first deployment (Postgres only)
    # - Only runs when a DATABASE_URL (Postgres) is configured
    # - Uses an advisory lock to prevent race conditions across workers
    # - Idempotent: only creates tables and seeds if no admin/cars exist
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    init_db_done = False

    if db_uri and db_uri.startswith('postgresql://'):
        try:
            from sqlalchemy import text

            engine = db.get_engine(app)
            with app.app_context():
                # Quick check: if admin exists, assume DB is initialized
                if Admin.query.first():
                    init_db_done = True
                else:
                    # Acquire advisory lock to ensure only one process runs initialization
                    lock_key = 987654321
                    with engine.connect() as conn:
                        try:
                            got_lock = conn.execute(text(f"SELECT pg_try_advisory_lock({lock_key})")).scalar()
                        except Exception:
                            got_lock = False

                        if got_lock:
                            # Create tables
                            db.create_all()

                            # Create default admin if not exists
                            if not Admin.query.filter_by(username='admin').first():
                                admin = Admin(username='admin', email='admin@carrental.com')
                                admin.set_password('admin')
                                db.session.add(admin)
                                db.session.commit()
                                app.logger.info("Default admin created: username='admin', password='admin'")

                            # Seed data only if no cars exist
                            from app.models import Car
                            if Car.query.count() == 0:
                                try:
                                    from seed_data import seed_database as _seed_database
                                    _seed_database()
                                    app.logger.info('Database seeded successfully during startup')
                                except Exception as e:
                                    app.logger.exception('Seeding failed during startup')

                            # Release advisory lock
                            try:
                                conn.execute(text(f"SELECT pg_advisory_unlock({lock_key})"))
                            except Exception:
                                pass

                            init_db_done = True
                        else:
                            app.logger.info('Another process is initializing the DB; skipping init in this worker')
        except Exception:
            app.logger.exception('Automatic DB initialization failed; skipping')

    # Fallback behavior for development or explicit flag
    if not init_db_done:
        init_db_flag = os.environ.get('INIT_DB', 'false').lower() == 'true'
        if app.config.get('DEBUG') or init_db_flag:
            with app.app_context():
                db.create_all()

                # Create default admin if not exists
                if not Admin.query.filter_by(username='admin').first():
                    admin = Admin(username='admin', email='admin@carrental.com')
                    admin.set_password('admin')
                    db.session.add(admin)
                    db.session.commit()
                    print("Default admin created: username='admin', password='admin'")

    # Register Blueprints - Web UI (Admin Only)
    from .presentation.auth.login import login_bp
    from .presentation.auth.logout import logout_bp
    from .presentation.admin.dashboard import admin_bp
    from .presentation.admin.add_car import add_car_bp
    from .presentation.admin.manage_fleet import manage_fleet_bp
    from .presentation.admin.tracking import tracking_bp
    from .presentation.admin.damage_claims import damage_claims_bp
    from .presentation.admin.bookings import bookings_bp
    from .presentation.admin.keyless import keyless_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(add_car_bp)
    app.register_blueprint(manage_fleet_bp)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(damage_claims_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(keyless_bp)

    # Attempt to register optional db init blueprint if present (non-fatal)
    try:
        from .presentation.admin.db_init import db_init_bp
        app.register_blueprint(db_init_bp)
        logger.info('Optional db_init blueprint registered')
    except Exception:
        logger.info('Optional db_init blueprint not found; continuing without it')
    
    # Register API Blueprints
    from .api.v1.cars import api_cars_bp
    from .api.v1.bookings import api_bookings_bp

    # Register public-facing customer blueprints
    try:
        from .presentation.customer.browse_cars import customer_bp
        from .presentation.customer.book_car import booking_bp
        app.register_blueprint(customer_bp)
        app.register_blueprint(booking_bp)
        logger.info('Customer blueprints registered')
    except Exception:
        logger.warning('Customer blueprints missing or failed to register')

    app.register_blueprint(api_cars_bp)
    app.register_blueprint(api_bookings_bp)
    
    logger.info('All blueprints registered successfully')

    # Add root route redirect to admin login
    @app.route('/')
    def index():
        return redirect(url_for('login.login'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f'404 error: {error}')
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'500 error: {error}')
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Custom exception handler
    from app.utils.exceptions import CarRentalException
    
    @app.errorhandler(CarRentalException)
    def handle_custom_exception(error):
        logger.error(f'Custom exception: {error.message}')
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    # Health check endpoint for monitoring
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'car-rental-system',
            'version': '1.0.0'
        }), 200
    
    logger.info('Application initialization complete')
    
    return app
