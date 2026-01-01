# Design Patterns Implementation Guide

This document details how each design pattern is implemented in the Car Rental System and demonstrates enterprise-level software architecture.

---

## 1. Abstract Factory Pattern

**Location:** `app/patterns/abstact_factory/`

### Purpose
Create families of related objects (vehicles) without specifying their concrete classes.

### Implementation

**Abstract Factory Interface:**
```python
class VehicleFactory(ABC):
    @abstractmethod
    def create_car(self):
        pass
    
    @abstractmethod
    def create_tracker(self):
        pass
    
    @abstractmethod
    def create_access_system(self):
        pass
    
    @abstractmethod
    def create_maintenance_profile(self):
        pass
```

**Concrete Factories:**
- `EconomyVehicleFactory` - Creates budget vehicle family
- `LuxuryVehicleFactory` - Creates premium vehicle family
- `SUVVehicleFactory` - Creates SUV vehicle family

### Real-World Usage
When adding a new car in `FleetService`:
```python
factory_class = FACTORY_MAP.get(category)  # Get factory
factory = factory_class()  # Instantiate
car_config = factory.create_car()  # Create family
tracker = factory.create_tracker()
access = factory.create_access_system()
maintenance = factory.create_maintenance_profile()
```

### Benefits
- ✅ Easy to add new vehicle categories
- ✅ Ensures consistency within product families
- ✅ Encapsulates object creation logic
- ✅ Follows Open/Closed Principle

---

## 2. State Pattern

**Location:** `app/patterns/state/`

### Purpose
Allow an object (Car) to change behavior when its internal state changes.

### Implementation

**State Interface:**
```python
class CarState(ABC):
    @abstractmethod
    def get_status_name(self):
        pass
    
    @abstractmethod
    def can_be_booked(self):
        pass
    
    @abstractmethod
    def can_be_serviced(self):
        pass
```

**Concrete States:**
- `AvailableState` - Car ready for booking
- `BookedState` - Car currently rented
- `InServiceState` - Car being serviced
- `MaintenanceState` - Car under maintenance
- `OutOfRangeState` - Car outside geofence

### State Transitions
```
Available ──book──> Booked ──return──> Available
    │                                      │
    └──service──> InService ──complete──┘
         │
         └──major──> Maintenance ──fix──> Available
```

### Real-World Usage
In `BookingService.create_booking()`:
```python
car = CarRepository.get_by_id(car_id)
if not car.state.can_be_booked():
    return {'success': False, 'message': 'Car unavailable'}
```

### Benefits
- ✅ Eliminates complex conditionals
- ✅ Each state encapsulates its behavior
- ✅ Easy to add new states
- ✅ State-specific validation

---

## 3. Strategy Pattern

**Location:** `app/patterns/strategy/`

### Purpose
Define a family of algorithms (pricing strategies) and make them interchangeable.

### Implementation

**Strategy Interface:**
```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, base_rate, days):
        pass
```

**Concrete Strategies:**
- `BasePricing` - Standard pricing
- `PeakPricing` - 30% markup for high demand
- `DiscountPricing` - 15% discount for 7+ days

### Real-World Usage
In `BookingService`:
```python
pricing_strategies = {
    'base': BasePricing(),
    'peak': PeakPricing(),
    'discount': DiscountPricing()
}

strategy = pricing_strategies.get(pricing_strategy)
price_info = strategy.calculate_price(car.price_tier, days)
```

### Benefits
- ✅ Runtime algorithm selection
- ✅ Eliminates pricing conditionals
- ✅ Easy to add new pricing models
- ✅ Testable strategies

---

## 4. Observer Pattern

**Location:** `app/patterns/observer/`

### Purpose
Define one-to-many dependency where state changes notify observers.

### Implementation

**Subject:**
```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self, event_type, data):
        for observer in self._observers:
            observer.update(event_type, data)
```

**Observers:**
- `AdminNotifier` - Sends notifications to admin
- `AlertLogger` - Logs events to file

### Real-World Usage
In `BookingService`:
```python
self.notification_system = Subject()
self.notification_system.notify('car_booked', {
    'car_id': car_id,
    'customer_name': customer_name
})
```

In `TrackingService` for geofencing:
```python
if is_out_of_range:
    self.notification_system.notify('geofence_breach', data)
```

### Benefits
- ✅ Loose coupling between components
- ✅ Easy to add new observers
- ✅ No modification to subject code
- ✅ Event-driven architecture

---

## 5. Chain of Responsibility

**Location:** `app/patterns/cor/`

### Purpose
Pass requests along a chain of handlers until one processes it.

### Implementation

**Handler Chain:**
```python
class DamageHandler(ABC):
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler):
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, claim):
        pass
```

**Concrete Handlers:**
1. `InsuranceHandler` - Handles insurance-covered claims
2. `MinorDamageHandler` - Handles < $500 damages
3. `MajorDamageHandler` - Handles >= $500 damages

### Chain Setup
```python
insurance = InsuranceHandler()
minor = MinorDamageHandler()
major = MajorDamageHandler()

insurance.set_next(minor).set_next(major)
```

### Real-World Usage
In `ClaimService`:
```python
handler = self._build_handler_chain()
result = handler.handle(claim_data)
```

### Benefits
- ✅ Decouples request sender/receiver
- ✅ Flexible handler ordering
- ✅ Single Responsibility Principle
- ✅ Easy to add new handlers

---

## 6. Proxy Pattern

**Location:** `app/patterns/proxy/`

### Purpose
Provide a surrogate for another object to control access.

### Implementation

**Real Subject:**
```python
class CarAccess:
    def unlock_car(self, car_id):
        # Actual unlock logic
        pass
```

**Proxy:**
```python
class AccessProxy:
    def __init__(self):
        self._car_access = CarAccess()
    
    def unlock_car(self, car_id, access_code):
        # Verify access code
        if not self._verify_code(access_code):
            raise UnauthorizedAccessException()
        
        # Log access attempt
        self._log_access(car_id)
        
        # Delegate to real subject
        return self._car_access.unlock_car(car_id)
```

### Real-World Usage
Used for secure car access with digital codes:
```python
proxy = AccessProxy()
try:
    proxy.unlock_car(car_id=5, access_code="ABC123")
except UnauthorizedAccessException:
    # Handle failed access
```

### Benefits
- ✅ Access control layer
- ✅ Logging and auditing
- ✅ Lazy initialization possible
- ✅ Protection proxy pattern

---

## 7. Repository Pattern

**Location:** `app/data/`

### Purpose
Mediate between domain and data mapping layers using collection-like interface.

### Implementation

**Repository Interface:**
```python
class CarRepository:
    @staticmethod
    def create(license_plate, model, category, ...):
        pass
    
    @staticmethod
    def get_by_id(car_id):
        pass
    
    @staticmethod
    def get_all():
        pass
    
    @staticmethod
    def update_status(car_id, new_status):
        pass
```

### Repositories:
- `CarRepository` - Car data operations
- `BookingRepository` - Booking data operations
- `ClaimRepository` - Claim data operations

### Real-World Usage
In services:
```python
car = CarRepository.get_by_id(car_id)  # Fetch
CarRepository.update_status(car_id, 'booked')  # Update
booking = BookingRepository.create(...)  # Create
```

### Benefits
- ✅ Separates business logic from data access
- ✅ Centralized data access logic
- ✅ Easy to swap databases
- ✅ Testable with mock repositories

---

## Pattern Interaction Diagram

```
Customer Request
    │
    ├──> BookingService
    │       │
    │       ├──> Strategy (Pricing)
    │       ├──> State (Car Availability)
    │       ├──> Repository (Data Access)
    │       └──> Observer (Notifications)
    │
    ├──> FleetService
    │       │
    │       ├──> Abstract Factory (Vehicle Creation)
    │       └──> Repository (Data Access)
    │
    └──> ClaimService
            │
            ├──> Chain of Responsibility (Claim Processing)
            ├──> Proxy (Access Control)
            └──> Repository (Data Access)
```

---

## Enterprise Benefits

### Code Quality
- **Maintainability**: Each pattern has single responsibility
- **Extensibility**: New features added without modifying existing code
- **Testability**: Patterns enable isolated unit testing
- **Readability**: Clear structure and intent

### Business Value
- **Scalability**: Patterns support growing complexity
- **Flexibility**: Easy to adapt to changing requirements
- **Reliability**: Well-tested pattern implementations
- **Team Collaboration**: Standard patterns improve communication

### Professional Standards
- ✅ Follows SOLID principles
- ✅ Gang of Four design patterns
- ✅ Domain-Driven Design
- ✅ Clean Architecture layers
- ✅ Enterprise application architecture

---

## Adding New Patterns

### Template Method (Future)
For standardized booking workflows:
```python
class BookingTemplate(ABC):
    def process_booking(self):
        self.validate_customer()
        self.check_availability()
        self.calculate_price()
        self.create_booking()
        self.send_confirmation()
```

### Decorator (Future)
For adding features to cars:
```python
class GPSDecorator(CarDecorator):
    def get_features(self):
        return super().get_features() + ['GPS Tracking']
```

### Singleton (Configuration)
For application configuration:
```python
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

## Learning Resources

- **Gang of Four Book**: "Design Patterns: Elements of Reusable Object-Oriented Software"
- **Head First Design Patterns**: Easier introduction
- **Refactoring Guru**: Visual pattern explanations
- **This Codebase**: Live examples in production context

---

**Note**: This system demonstrates patterns not as academic exercises, but as practical solutions to real business problems in car rental management.
