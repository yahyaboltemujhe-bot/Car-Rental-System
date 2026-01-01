# Car Rental System - AI Agent Instructions

## Architecture Overview

This is a Flask-based car rental management system built with a **domain-driven, pattern-centric architecture**. The codebase emphasizes design patterns as first-class architectural components rather than implementation details.

### Core Layers

- **Presentation** (`app/presentation/`): Flask blueprints organized by feature area (auth, admin)
  - Auth routes: `/auth/*` via `login_bp` blueprint
  - Admin routes: `/admin/*` via `admin_bp` blueprint
  - Each blueprint maps to templates in `templates/{auth,admin}/`
- **Services** (`app/services/`): Business logic orchestration layer
- **Domain** (`app/domain/`): Core entities (Car, Booking, Access, Location)
- **Data** (`app/data/`): Repository pattern for data access (`*_repository.py`)
- **Patterns** (`app/patterns/`): Design pattern implementations (see below)

## Critical Design Patterns

This project **explicitly implements Gang of Four patterns** as core architectural components. When adding features, you MUST extend the existing pattern structure:

### Abstract Factory (`patterns/abstact_factory/`)
- **Purpose**: Creates vehicle families (Economy, Luxury, SUV) with associated components
- **Base**: `VehicleFactory` defines 4 factory methods: `create_car()`, `create_tracker()`, `create_access_system()`, `create_maintenance_profile()`
- **Implementations**: `economy_vehicle_factory.py`, `luxury_vehicle_factory.py`, `suv_vehicle_factory.py`
- **When to use**: Adding new vehicle categories or vehicle-related component types

### State Pattern (`patterns/state/`)
- **Purpose**: Manages car availability states (Available, Booked, In Service, Maintenance, Out of Range)
- **Files**: `car_state.py` (base), `available.py`, `booked.py`, `in_service.py`, `maintenance.py`, `out_of_range.py`
- **When to use**: Implementing state-dependent car behaviors or adding new states

### Observer Pattern (`patterns/observer/`)
- **Purpose**: Notification system for system events
- **Components**: `subject.py` (publisher), `admin_notifier.py`, `alert_logger.py` (observers)
- **When to use**: Adding new notification channels or event types

### Chain of Responsibility (`patterns/cor/`)
- **Purpose**: Damage claim processing pipeline
- **Chain**: `damage_handler.py` (base) → `insurance_handler.py` → `minor_damage.py` → `major_damage.py`
- **When to use**: Adding new damage assessment criteria or claim processing steps

### Proxy Pattern (`patterns/proxy/`)
- **Purpose**: Access control and authentication
- **Files**: `car_access.py` (real subject), `access_proxy.py` (proxy wrapper)
- **When to use**: Adding authorization layers or access logging

## Project Conventions

### File Organization
- **Blueprint naming**: `{feature}_bp` (e.g., `login_bp`, `admin_bp`)
- **Repository naming**: `{entity}_repository.py` (e.g., `car_repository.py`, `booking_repository.py`)
- **Service naming**: `{feature}_service.py` (e.g., `fleet_service.py`, `tracking_service.py`)
- **CSS organization**: Mirrors template structure (`static/css/admin/`, `static/css/auth/`)

### Application Entry Points
- **Main entry**: `run.py` → calls `create_app()` from `app/__init__.py`
- **App factory**: `app/__init__.py` registers all blueprints in `create_app()`
- **Database**: SQLite at `database/car_rental.db`

## Development Workflow

### Running the Application
```bash
python run.py  # Starts Flask dev server with debug=True
```

### Adding New Features
1. **New admin feature**: Create blueprint in `app/presentation/admin/{feature}.py`
2. **Register blueprint**: Add to `app/__init__.py` in `create_app()`
3. **Add template**: Create matching template in `templates/admin/{feature}.html`
4. **Add styles**: Create CSS file in `static/css/admin/{feature}.css`
5. **If pattern-based logic needed**: Extend appropriate pattern in `app/patterns/`

### Pattern Extension Example
When adding a new vehicle type (e.g., "Van"):
- Create `patterns/abstact_factory/van_vehicle_factory.py`
- Implement all 4 abstract methods from `VehicleFactory`
- Update service layer to use new factory

## Important Notes

- **Pattern-first approach**: This codebase uses design patterns as structural elements, not just implementation techniques
- **Empty scaffolding**: Many files are currently placeholders - follow established naming and structure when implementing
- **Blueprint registration**: All new blueprints MUST be registered in `app/__init__.py` to be accessible
- **Template-CSS pairing**: Every template should have a corresponding CSS file in mirrored directory structure
