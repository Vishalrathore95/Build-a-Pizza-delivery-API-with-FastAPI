# Pizza Delivery API

A FastAPI-based REST API for managing pizza orders with user authentication and order management.

## Features

- User registration and authentication with JWT tokens
- Pizza order management (create, view, update status)
- Multiple pizza sizes (Small, Medium, Large, Extra-Large)
- Order status tracking (Pending, In-Transit, Delivered)
- SQLAlchemy ORM with database integration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Build a Pizza delivery API with FastAPI"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

#### Register User
```http
POST /auth/signup
Content-Type: application/json

{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "password123"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "password123"
}
```

### Orders

#### Create Order
```http
POST /order/
Authorization: Bearer <token>
Content-Type: application/json

{
  "quantity": 2,
  "pizza_size": "MEDIUM"
}
```

#### Get User Orders
```http
GET /order/user/orders
Authorization: Bearer <token>
```

## Pizza Sizes

- `SMALL`
- `MEDIUM`
- `LARGE`
- `EXTRA-LARGE`

## Order Status

- `PENDING` - Order placed, awaiting preparation
- `IN-TRANSIT` - Order is being delivered
- `DELIVERED` - Order completed

## Testing

Run the test script to verify API functionality:

```bash
python test_api.py
```

Make sure to update the credentials in `test_api.py` with valid user credentials.

## Project Structure

```
├── main.py              # FastAPI application entry point
├── auth_routes.py       # Authentication endpoints
├── order_routes.py      # Order management endpoints
├── models.py           # SQLAlchemy database models
├── schemas.py          # Pydantic schemas for request/response
├── database.py         # Database configuration
├── requirements.txt    # Python dependencies
└── test_api.py        # API testing script
```

## Technologies Used

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **JWT** - JSON Web Tokens for authentication
- **bcrypt** - Password hashing
- **Uvicorn** - ASGI server implementation

## License

This project is open source and available under the MIT License.
