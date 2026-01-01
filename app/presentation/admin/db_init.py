from flask import Blueprint, request, jsonify, current_app
import os

# Import the initialization functions
import init_db as _init_db
import seed_data as _seed_data

db_init_bp = Blueprint('db_init', __name__, url_prefix='/internal')

@db_init_bp.route('/init-db', methods=['POST'])
def init_db_route():
    """Protected endpoint to initialize and seed the database.

    Security: Only enabled when ENABLE_DB_INIT=true and the request contains
    the correct token via header X-INIT-TOKEN or query param `token`.

    IMPORTANT: Remove or disable this endpoint after use.
    """
    # Feature flag
    if os.environ.get('ENABLE_DB_INIT', 'false').lower() != 'true':
        return jsonify({'error': 'DB init is disabled'}), 403

    token = os.environ.get('INIT_DB_TOKEN')
    req_token = request.headers.get('X-INIT-TOKEN') or request.args.get('token')

    if not token or not req_token or req_token != token:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        # Run the init and seed functions
        _init_db.init_database()
        _seed_data.seed_database()
        current_app.logger.info('Database initialized and seeded via /internal/init-db')
        return jsonify({'status': 'ok', 'message': 'Database initialized and seeded'}), 200
    except Exception as e:
        current_app.logger.exception('DB init failed')
        return jsonify({'status': 'error', 'message': str(e)}), 500
