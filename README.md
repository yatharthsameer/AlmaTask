# Lead Management System - Setup Guide

Demo Video: https://www.loom.com/share/f6aa5562a04a49f3ba7cc7d5708393d2?sid=6360bdc5-eda7-42b3-9024-dc62e19bd7e2


## Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

## Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yatharthsameer/AlmaTask.git
cd AlmaTask
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the root directory with the following content:
```env
# JWT Settings
JWT_SECRET=your_secret_key
JWT_ALGORITHM=HS256

# Email Settings
ATTORNEY_EMAIL=thesameerbros@gmail.com
SMTP_USERNAME=your_gmail_username
SMTP_PASSWORD=your_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

Note: For Gmail, you'll need to generate an App Password. Do not use your regular Gmail password.

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The application will start on `http://localhost:8000`

## Testing the Application

1. **Submit a Lead (Public Endpoint)**
```bash
curl -X POST http://localhost:8000/api/leads \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "email=john@example.com" \
  -F "resume=@/path/to/resume.pdf"
```

2. **Login (Get JWT Token)**
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"
```

3. **List Leads (Protected Endpoint)**
```bash
curl -X GET http://localhost:8000/api/leads \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

4. **Update Lead Status (Protected Endpoint)**
```bash
curl -X PATCH http://localhost:8000/api/leads/{lead_id}/status \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "REACHED_OUT"}'
```

5. **Test Email Functionality**
```bash
curl -X POST http://localhost:8000/api/test/email \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Troubleshooting

1. **Email Issues**
- Check if SMTP credentials are correct in `.env`
- Verify that you're using an App Password for Gmail
- Check spam folder for test emails

2. **Authentication Issues**
- Ensure JWT_SECRET is properly set in `.env`
- Verify that the JWT token is included in the Authorization header
- Check if the token has expired

3. **File Upload Issues**
- Ensure the upload directory exists and has proper permissions
- Check if the file size is within acceptable limits
