# Lead Management System - API Documentation

## API Endpoints

### Public Endpoints

#### Submit Lead
```
POST /api/leads
Content-Type: multipart/form-data

Parameters:
- first_name (string, required)
- last_name (string, required)
- email (string, required)
- resume (file, required)

Response:
{
    "id": "unique_lead_id"
}
```

### Protected Endpoints

#### Login
```
POST /api/login
Content-Type: application/x-www-form-urlencoded

Parameters:
- username (string, required)
- password (string, required)

Response:
{
    "access_token": "jwt_token",
    "token_type": "bearer"
}
```

#### List Leads
```
GET /api/leads
Authorization: Bearer {token}

Query Parameters:
- status (string, optional): Filter by lead status

Response:
[
    {
        "id": "unique_lead_id",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "resume_path": "/path/to/resume.pdf",
        "status": "PENDING",
        "created_at": "2025-02-22T02:55:41"
    }
]
```

#### Update Lead Status
```
PATCH /api/leads/{lead_id}/status
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
    "status": "REACHED_OUT"
}

Response:
{
    "id": "unique_lead_id",
    "status": "REACHED_OUT",
    "updated_at": "2025-02-22T02:55:41"
}
```

#### Get Resume
```
GET /api/leads/{lead_id}/resume
Authorization: Bearer {token}

Response:
Binary file content (application/pdf or application/msword)
```

#### Test Email
```
POST /api/test/email
Authorization: Bearer {token}

Response:
{
    "message": "Test emails triggered"
}
```

## Data Models

### Lead
```python
{
    "id": str,
    "first_name": str,
    "last_name": str,
    "email": str,
    "resume_path": str,
    "status": Enum["PENDING", "REACHED_OUT"],
    "created_at": datetime,
    "updated_at": datetime
}
```

## Authentication

The API uses JWT (JSON Web Token) authentication. Protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...
```

To obtain a token, use the login endpoint with the provided credentials.

## Email Notifications

The system sends two types of email notifications:

1. **Prospect Email**
   - Sent to the lead's email address
   - Confirms submission receipt
   - Contains a thank you message

2. **Attorney Email**
   - Sent to the configured attorney email
   - Contains lead details
   - Notifies of new submission

## Error Handling

The API returns standard HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

Error responses include a detail message:
```json
{
    "detail": "Error description"
}
```
