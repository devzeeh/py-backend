# Py Backend

This is a Flask-based backend project created as a learning and practice exercise. It was helped and guided by Gemini AI during development, with the goal of learning backend fundamentals such as authentication, database integration, validation, rate limiting, and API structure.

## Overview

The project provides a simple but functional API for:

- user registration
- login with JWT authentication
- protected profile access
- task creation, listing, updating, and deletion
- input validation with Pydantic
- request rate limiting with Flask-Limiter
- database handling with Flask-SQLAlchemy
- test coverage for core auth behavior

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Limiter
- Flask-Migrate
- Pydantic
- SQLite (default for local development)
- pytest

## Project Structure

```bash
py-backend/
├── app.py
├── config.py
├── extensions.py
├── main.py
├── requirements.txt
├── README.md
├── api/
│   ├── errors.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
├── migrations/
├── instance/
├── tests/
│   ├── test_auth.py
│   └── test_limiter.py
└── py-api test/
```

## Features

### Authentication
- Register a new user
- Log in with email and password
- Receive a JWT access token
- Access protected endpoints using the token

### Task Management
- Create a task
- Get tasks for the logged-in user
- Filter tasks by completion status
- Update task title or completion state
- Delete a task

### Security and Validation
- Password hashing
- JWT-based protected routes
- Input validation for request payloads
- Request rate limiting to reduce abuse

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Configuration

The app uses environment variables and a default config file. You can create a `.env` file if needed, for example:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
PORT=5000
```

## Run the App

```bash
python app.py
```

Or run the app using Flask CLI:

```bash
flask run
```

By default, the API will be available at:

```bash
http://localhost:5000
```

## API Endpoints

### Public Routes

- `POST /api/v1/register`
- `POST /api/v1/login`
- `POST /api/v1/greet`
- `GET /api/v1/users`

### Protected Routes

- `GET /api/v1/profile`
- `GET /api/v1/tasks`
- `POST /api/v1/tasks`
- `PUT /api/v1/tasks/<task_id>`
- `DELETE /api/v1/tasks/<task_id>`

## Example Request

### Register User

```bash
curl -X POST http://localhost:5000/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

## Testing

Run the test suite with:

```bash
pytest
```

## Notes

This project is mainly intended for practice and learning backend development concepts. It demonstrates a clean Flask API structure and the integration of common patterns used in real-world backend systems.

The project was developed with support from Gemini AI as part of hands-on learning and code practice.
