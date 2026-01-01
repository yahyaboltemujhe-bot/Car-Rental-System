"""
Seed database with sample cars, bookings, and claims for testing
"""
from app import create_app, db
from app.models import Car, Booking, Claim, Admin
from app.services.fleet_service import FleetService
from app.services.booking_service import BookingService
from app.services.claim_service import ClaimService
from datetime import datetime, timedelta

def seed_database():
    """Populate database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Claim.query.delete()
        Booking.query.delete()
        Car.query.delete()
        
        # Keep admin user
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin')
            admin.set_password('admin')
            db.session.add(admin)
        
        db.session.commit()
        print("✓ Database cleared")
        
        # Add sample cars using Fleet Service
        fleet_service = FleetService()
        print("\nAdding sample cars...")
        
        sample_cars = [
            # Economy vehicles
            {'license_plate': 'ECO001', 'model': 'Toyota Corolla 2023', 'category': 'economy', 
             'rental_lat': 40.7128, 'rental_lng': -74.0060},  # New York
            {'license_plate': 'ECO002', 'model': 'Honda Civic 2022', 'category': 'economy',
             'rental_lat': 40.7128, 'rental_lng': -74.0060},
            {'license_plate': 'ECO003', 'model': 'Hyundai Elantra 2023', 'category': 'economy',
             'rental_lat': 40.7128, 'rental_lng': -74.0060},
            
            # Luxury vehicles
            {'license_plate': 'LUX001', 'model': 'BMW 7 Series 2024', 'category': 'luxury',
             'rental_lat': 34.0522, 'rental_lng': -118.2437},  # Los Angeles
            {'license_plate': 'LUX002', 'model': 'Mercedes S-Class 2023', 'category': 'luxury',
             'rental_lat': 34.0522, 'rental_lng': -118.2437},
            {'license_plate': 'LUX003', 'model': 'Audi A8 2024', 'category': 'luxury',
             'rental_lat': 34.0522, 'rental_lng': -118.2437},
            
            # SUV vehicles
            {'license_plate': 'SUV001', 'model': 'Toyota RAV4 2023', 'category': 'suv',
             'rental_lat': 41.8781, 'rental_lng': -87.6298},  # Chicago
            {'license_plate': 'SUV002', 'model': 'Honda CR-V 2024', 'category': 'suv',
             'rental_lat': 41.8781, 'rental_lng': -87.6298},
            {'license_plate': 'SUV003', 'model': 'Jeep Grand Cherokee 2023', 'category': 'suv',
             'rental_lat': 41.8781, 'rental_lng': -87.6298},
        ]
        
        cars_added = []
        for car_data in sample_cars:
            result = fleet_service.add_car(**car_data)
            if result['success']:
                car = result['car']
                cars_added.append(car)
                print(f"  ✓ Added {car.license_plate} - {car.model} ({car.category})")
        
        print(f"\n✓ Added {len(cars_added)} cars")
        
        # Add sample bookings
        print("\nCreating sample bookings...")
        booking_service = BookingService()
        
        bookings_data = [
            # Active bookings
            {'car_id': cars_added[0].id, 'customer_name': 'John Smith', 
             'customer_email': 'john@example.com', 'days': 5, 'pricing_strategy': 'base'},
            {'car_id': cars_added[3].id, 'customer_name': 'Sarah Johnson', 
             'customer_email': 'sarah@example.com', 'days': 3, 'pricing_strategy': 'peak'},
            {'car_id': cars_added[6].id, 'customer_name': 'Mike Davis', 
             'customer_email': 'mike@example.com', 'days': 7, 'pricing_strategy': 'discount'},
            
            # Completed bookings
            {'car_id': cars_added[1].id, 'customer_name': 'Emma Wilson', 
             'customer_email': 'emma@example.com', 'days': 4, 'pricing_strategy': 'base'},
            {'car_id': cars_added[4].id, 'customer_name': 'David Brown', 
             'customer_email': 'david@example.com', 'days': 2, 'pricing_strategy': 'peak'},
        ]
        
        bookings_created = []
        for i, booking_data in enumerate(bookings_data):
            result = booking_service.create_booking(**booking_data)
            if result['success']:
                booking = result['booking']
                
                # Mark last 2 as completed (past bookings)
                if i >= 3:
                    booking.end_date = datetime.utcnow() - timedelta(days=2)
                    booking.is_active = False
                    # Return car to available
                    car = Car.query.get(booking.car_id)
                    if car:
                        from app.patterns.state.available import AvailableState
                        car.state = AvailableState()
                        car.status = 'available'
                
                bookings_created.append(booking)
                db.session.add(booking)
                print(f"  ✓ Booking {booking.id} for {booking.customer_name} - ${booking.total_cost}")
        
        db.session.commit()
        print(f"\n✓ Created {len(bookings_created)} bookings")
        
        # Add sample damage claims
        print("\nFiling sample damage claims...")
        claim_service = ClaimService()
        
        claims_data = [
            # Minor damage
            {'car_id': cars_added[1].id, 'booking_id': bookings_created[3].id,
             'damage_type': 'Minor Scratch', 'description': 'Small scratch on rear bumper',
             'estimated_cost': 250.00},
            
            # Major damage
            {'car_id': cars_added[4].id, 'booking_id': bookings_created[4].id,
             'damage_type': 'Dent', 'description': 'Large dent on driver side door',
             'estimated_cost': 1500.00},
            
            # Insurance claim
            {'car_id': cars_added[2].id, 'booking_id': None,
             'damage_type': 'Collision', 'description': 'Front end collision damage',
             'estimated_cost': 4500.00},
            
            # Pending minor
            {'car_id': cars_added[5].id, 'booking_id': None,
             'damage_type': 'Interior Damage', 'description': 'Stain on rear seat',
             'estimated_cost': 150.00},
        ]
        
        claims_created = []
        for i, claim_data in enumerate(claims_data):
            result = claim_service.file_claim(**claim_data)
            if result['success']:
                claim = result['claim']
                
                # Approve first 2 claims
                if i < 2:
                    claim_service.approve_claim(claim.id)
                
                claims_created.append(claim)
                print(f"  ✓ Claim {claim.id} - {claim.damage_type} (${claim.estimated_cost})")
                print(f"    Handler: {result['processing_result']['handler']}")
        
        print(f"\n✓ Filed {len(claims_created)} damage claims")
        
        # Update some cars to different states
        print("\nSetting car states...")
        
        # Set one car to maintenance
        cars_added[2].status = 'maintenance'
        from app.patterns.state.maintenance import MaintenanceState
        cars_added[2].state = MaintenanceState()
        
        # Set one car to in_service
        cars_added[5].status = 'in_service'
        from app.patterns.state.in_service import InServiceState
        cars_added[5].state = InServiceState()
        
        db.session.commit()
        print("  ✓ Updated car states")
        
        # Summary
        print("\n" + "="*60)
        print("DATABASE SEEDING COMPLETE!")
        print("="*60)
        print(f"✓ Cars: {len(cars_added)}")
        print(f"  - Economy: {len([c for c in cars_added if c.category == 'economy'])}")
        print(f"  - Luxury: {len([c for c in cars_added if c.category == 'luxury'])}")
        print(f"  - SUV: {len([c for c in cars_added if c.category == 'suv'])}")
        print(f"\n✓ Bookings: {len(bookings_created)}")
        print(f"  - Active: {len([b for b in bookings_created if b.is_active])}")
        print(f"  - Completed: {len([b for b in bookings_created if not b.is_active])}")
        print(f"\n✓ Claims: {len(claims_created)}")
        print(f"  - Pending: {len([c for c in claims_created if c.status == 'pending'])}")
        print(f"  - Approved: {len([c for c in claims_created if c.status == 'approved'])}")
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin")
        print("="*60)

if __name__ == '__main__':
    seed_database()
