# Lead Management System - Design Document

## System Architecture

### Overview
This Lead Management System is designed as a FastAPI-based REST API that handles lead submissions, email notifications, and lead management. The system follows a modular architecture with clear separation of concerns.

### Assumption
We consider for simplicity we have only 1 attorney, and he handles the leads. The system is designed to be scalable and can be extended to support multiple attorneys and teams.

### Components


1. **API Layer (`main.py`)**
   - Handles HTTP requests and responses
   - Implements input validation
   - Manages authentication and authorization
   - Coordinates between different services

2. **Authentication Service (`auth.py`)**
   - Implements JWT-based authentication
   - Handles user authentication
   - Manages token generation and validation

3. **Database Layer (`database.py`, `models.py`)**
   - Manages data persistence
   - Implements in-memory storage for MVP
   - Defines data models and relationships

4. **Email Service (`email_service.py`)**
   - Handles email notifications
   - Implements threading for non-blocking email sending
   - Manages SMTP connections and retries

5. **Schema Layer (`schemas.py`)**
   - Defines data validation schemas
   - Handles request/response models
   - Implements data transformation

### Design Decisions

1. **Choice of FastAPI**
   - Async-first framework
   - Built-in OpenAPI documentation
   - Strong type hints and validation

2. **Authentication Implementation**
   - JWT-based authentication for stateless operation
   - Simple username/password for MVP
   - Token-based API access for protected endpoints

3. **Email Service Design**
   - Standard `smtplib` over `aiosmtplib` for reliability
   - Threading implementation to prevent blocking

4. **Storage Implementation**
   - In-memory storage for MVP simplicity
   - File system storage for resumes

5. **Lead Status Management**
   - Simple state machine (PENDING → REACHED_OUT)
   - Manual status updates by attorneys
   - Audit trail through timestamps

### Security Considerations

**Authentication & Authorization**
   - JWT tokens with expiration
   - Protected routes for internal operations
   - Public routes for lead submission only

