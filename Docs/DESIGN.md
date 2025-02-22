# Lead Management System - Design Document

## System Architecture

### Overview
The Lead Management System is designed as a FastAPI-based REST API that handles lead submissions, email notifications, and lead management. The system follows a modular architecture with clear separation of concerns.

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
   - Modern, async-first framework
   - Built-in OpenAPI documentation
   - Strong type hints and validation
   - High performance and scalability

2. **Authentication Implementation**
   - JWT-based authentication for stateless operation
   - Simple username/password for MVP
   - Token-based API access for protected endpoints

3. **Email Service Design**
   - Standard `smtplib` over `aiosmtplib` for reliability
   - Threading implementation to prevent blocking
   - Detailed logging for troubleshooting
   - Configurable SMTP settings via environment variables

4. **Storage Implementation**
   - In-memory storage for MVP simplicity
   - File system storage for resumes
   - Easily extensible to persistent storage

5. **Lead Status Management**
   - Simple state machine (PENDING → REACHED_OUT)
   - Manual status updates by attorneys
   - Audit trail through timestamps

### Security Considerations

1. **Authentication & Authorization**
   - JWT tokens with expiration
   - Protected routes for internal operations
   - Public routes for lead submission only

2. **File Upload Security**
   - File type validation
   - Size limits on uploads
   - Secure file storage implementation

3. **Email Security**
   - SMTP with TLS
   - App Password authentication
   - Environment variable configuration

### Scalability Considerations

1. **Async Operations**
   - Non-blocking email sending
   - Background task processing
   - Efficient request handling

2. **Storage Scalability**
   - Designed for easy migration to persistent storage
   - Separate file storage for attachments
   - Modular database interface

3. **Performance Optimizations**
   - Efficient in-memory operations
   - Background task processing
   - Connection pooling for SMTP

### Future Improvements

1. **Database Migration**
   - Implement persistent storage (e.g., PostgreSQL)
   - Add database migrations
   - Implement connection pooling

2. **Enhanced Authentication**
   - Role-based access control
   - OAuth integration
   - Multi-factor authentication

3. **Advanced Features**
   - Lead scoring
   - Automated follow-ups
   - Analytics dashboard
   - Email template management
