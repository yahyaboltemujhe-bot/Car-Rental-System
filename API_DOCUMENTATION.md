# API Documentation - Car Rental System v1.0

## Base URL
```
http://127.0.0.1:5000/api/v1
```

## Authentication

### API Key Authentication
Protected endpoints require an API key in the request header:
```http
X-API-Key: your-api-key-here
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## Cars Endpoints

### 1. Get All Cars

**Endpoint:** `GET /cars/`

**Description:** Retrieve a list of all cars with optional filtering and pagination.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter by status (available, booked, in_service, maintenance, out_of_range) |
| category | string | No | Filter by category (economy, luxury, suv) |
| limit | integer | No | Maximum number of results (default: 50) |
| offset | integer | No | Pagination offset (default: 0) |

**Example Request:**
```bash
curl "http://127.0.0.1:5000/api/v1/cars/?status=available&category=luxury&limit=10"
```

**Example Response:**
```json
{
  "success": true,
  "total": 25,
  "limit": 10,
  "offset": 0,
  "data": [
    {
      "id": 1,
      "license_plate": "ABC-123",
      "model": "Mercedes-Benz S-Class 2023",
      "category": "luxury",
      "status": "available",
      "price_tier": 2.0,
      "daily_rate": 100,
      "location": {
        "latitude": 40.7128,
        "longitude": -74.0060
      }
    }
  ]
}
```

---

### 2. Get Specific Car

**Endpoint:** `GET /cars/<car_id>`

**Description:** Retrieve detailed information about a specific car.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| car_id | integer | Yes | Car ID |

**Example Request:**
```bash
curl "http://127.0.0.1:5000/api/v1/cars/1"
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "license_plate": "ABC-123",
    "model": "Mercedes-Benz S-Class 2023",
    "category": "luxury",
    "status": "available",
    "price_tier": 2.0,
    "daily_rate": 100,
    "location": {
      "current": {
        "latitude": 40.7128,
        "longitude": -74.0060
      },
      "rental": {
        "latitude": 40.7128,
        "longitude": -74.0060
      }
    },
    "created_at": "2025-01-01T10:00:00"
  }
}
```

---

### 3. Get Available Cars

**Endpoint:** `GET /cars/available`

**Description:** Retrieve all cars currently available for booking.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| category | string | No | Filter by category |
| min_price | float | No | Minimum daily rate |
| max_price | float | No | Maximum daily rate |

**Example Request:**
```bash
curl "http://127.0.0.1:5000/api/v1/cars/available?category=economy&max_price=50"
```

**Example Response:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": 3,
      "license_plate": "ECO-001",
      "model": "Toyota Corolla 2023",
      "category": "economy",
      "daily_rate": 30,
      "location": {
        "latitude": 40.7128,
        "longitude": -74.0060
      }
    }
  ]
}
```

---

### 4. Get Fleet Statistics

**Endpoint:** `GET /cars/statistics`

**Description:** Get fleet-wide statistics (requires API key).

**Headers:**
```http
X-API-Key: your-api-key-here
```

**Example Request:**
```bash
curl -H "X-API-Key: your-api-key" "http://127.0.0.1:5000/api/v1/cars/statistics"
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "total": 15,
    "available": 8,
    "booked": 5,
    "in_service": 1,
    "maintenance": 1,
    "out_of_range": 0
  }
}
```

---

## Bookings Endpoints

### 1. Create Booking

**Endpoint:** `POST /bookings/`

**Description:** Create a new car booking.

**Request Body:**
```json
{
  "car_id": 1,
  "customer_name": "John Doe",
  "customer_phone": "03001234567",
  "customer_cnic": "12345-1234567-1",
  "start_date": "2025-01-10",
  "end_date": "2025-01-15",
  "pricing_strategy": "base"
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| car_id | integer | Yes | ID of the car to book |
| customer_name | string | Yes | Customer's full name |
| customer_phone | string | Yes | Phone number (03XX-XXXXXXX format) |
| customer_cnic | string | Yes | CNIC number (12345-1234567-1 format) |
| start_date | string | Yes | Start date (YYYY-MM-DD) |
| end_date | string | Yes | End date (YYYY-MM-DD) |
| pricing_strategy | string | No | "base", "peak", or "discount" (default: "base") |

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "car_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "03001234567",
    "customer_cnic": "12345-1234567-1",
    "start_date": "2025-01-10",
    "end_date": "2025-01-15",
    "pricing_strategy": "base"
  }'
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "booking_id": 1,
    "access_code": "AbCdEf123",
    "car_id": 1,
    "customer_name": "John Doe",
    "start_date": "2025-01-10",
    "end_date": "2025-01-15",
    "total_amount": 500.0,
    "status": "active",
    "pricing_details": {
      "daily_rate": 100,
      "days": 5,
      "subtotal": 500,
      "discount": 0,
      "total": 500
    }
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields or invalid data
- `404 Not Found`: Car not found
- `409 Conflict`: Car not available

---

### 2. Get Booking Details

**Endpoint:** `GET /bookings/<booking_id>`

**Description:** Retrieve booking details with optional access code verification.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| booking_id | integer | Yes | Booking ID |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| access_code | string | No | Access code for full details |

**Example Request:**
```bash
curl "http://127.0.0.1:5000/api/v1/bookings/1?access_code=AbCdEf123"
```

**Example Response (with access code):**
```json
{
  "success": true,
  "data": {
    "booking_id": 1,
    "car_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "03001234567",
    "start_date": "2025-01-10",
    "end_date": "2025-01-15",
    "total_amount": 500.0,
    "status": "active",
    "access_code": "AbCdEf123",
    "created_at": "2025-01-01T10:00:00"
  }
}
```

**Example Response (without access code):**
```json
{
  "success": true,
  "data": {
    "booking_id": 1,
    "car_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "03001234567",
    "start_date": "2025-01-10",
    "end_date": "2025-01-15",
    "total_amount": 500.0,
    "status": "active",
    "created_at": "2025-01-01T10:00:00"
  }
}
```

---

### 3. Verify Booking

**Endpoint:** `POST /bookings/verify`

**Description:** Verify a booking using booking ID and access code.

**Request Body:**
```json
{
  "booking_id": 1,
  "access_code": "AbCdEf123"
}
```

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/bookings/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": 1,
    "access_code": "AbCdEf123"
  }'
```

**Example Response:**
```json
{
  "success": true,
  "verified": true
}
```

---

## Health Check

### Health Endpoint

**Endpoint:** `GET /health`

**Description:** Check if the API service is running.

**Example Request:**
```bash
curl "http://127.0.0.1:5000/health"
```

**Example Response:**
```json
{
  "status": "healthy",
  "service": "car-rental-system",
  "version": "1.0.0"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid API key |
| 403 | Forbidden - Invalid access code |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource unavailable |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, no rate limiting is implemented. In production:
- Implement rate limiting per IP address
- Set reasonable limits (e.g., 100 requests/minute)
- Return 429 status for exceeded limits

---

## CORS Policy

The API supports Cross-Origin Resource Sharing (CORS) for all `/api/*` endpoints:
- Allowed Origins: `*` (all origins in development)
- In production: Restrict to specific domains

---

## Testing with Postman

Import the following collection structure:

```
Car Rental API v1
├── Cars
│   ├── Get All Cars
│   ├── Get Car by ID
│   ├── Get Available Cars
│   └── Get Statistics (requires API key)
└── Bookings
    ├── Create Booking
    ├── Get Booking
    └── Verify Booking
```

---

## SDK Examples

### Python
```python
import requests

# Get available cars
response = requests.get('http://127.0.0.1:5000/api/v1/cars/available')
cars = response.json()['data']

# Create booking
booking_data = {
    "car_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "03001234567",
    "customer_cnic": "12345-1234567-1",
    "start_date": "2025-01-10",
    "end_date": "2025-01-15"
}
response = requests.post(
    'http://127.0.0.1:5000/api/v1/bookings/',
    json=booking_data
)
booking = response.json()['data']
print(f"Booking ID: {booking['booking_id']}")
print(f"Access Code: {booking['access_code']}")
```

### JavaScript (Fetch API)
```javascript
// Get available cars
fetch('http://127.0.0.1:5000/api/v1/cars/available')
  .then(response => response.json())
  .then(data => console.log(data.data));

// Create booking
const bookingData = {
  car_id: 1,
  customer_name: "John Doe",
  customer_phone: "03001234567",
  customer_cnic: "12345-1234567-1",
  start_date: "2025-01-10",
  end_date: "2025-01-15"
};

fetch('http://127.0.0.1:5000/api/v1/bookings/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(bookingData)
})
  .then(response => response.json())
  .then(data => console.log(data.data));
```

---

## Changelog

### Version 1.0.0 (2025-01-01)
- Initial release
- Cars API endpoints
- Bookings API endpoints
- Health check endpoint
- CORS support
- Error handling

---

## Support

For issues or questions:
- Check the README.md
- Review error messages in response
- Enable debug logging
- Check logs/app.log for details
