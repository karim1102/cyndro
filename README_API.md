# Cyndro Pilot Program API

FastAPI backend for storing pilot program signups.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
# Option 1: Using uvicorn directly
uvicorn main:app --reload

# Option 2: Using the run script
python run_server.py
```

The API will be available at `http://localhost:8000`

## Frontend Integration

The HTML form in `landing_page_V3.html` is already configured to submit to the API. Make sure:

1. The FastAPI server is running
2. Update the API URL in the HTML file (line ~210) if deploying to production:
   ```javascript
   const API_URL = 'https://your-api-domain.com/api/signup';
   ```

## API Endpoints

### POST `/api/signup`
Create a new pilot program signup.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2025-01-XX..."
}
```

### GET `/api/signups`
Get all signups (for admin purposes).

### GET `/api/signups/{signup_id}`
Get a specific signup by ID.

### GET `/health`
Health check endpoint.

## Database

The database is stored in `pilot_program.db` (SQLite). The table is automatically created on first run.

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

