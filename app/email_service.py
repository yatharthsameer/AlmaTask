import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import threading
from .models import Lead

logger = logging.getLogger(__name__)

# Email configuration
ATTORNEY_EMAIL = os.getenv("ATTORNEY_EMAIL", "thesameerbros@gmail.com")
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "ytharthsmr@gmail.com")
SMTP_PASSWORD = "ihqr ymgt cnpa oyul"
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

def _send_email_sync(to_email: str, subject: str, body: str):
    """Send email using standard smtplib instead of aiosmtplib"""
    try:
        message = MIMEMultipart()
        message["From"] = SMTP_USERNAME
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Log connection attempt for debugging
        logger.info(f"Attempting to connect to SMTP server {SMTP_SERVER}:{SMTP_PORT}")
        
        # Get password from environment or .env file
        smtp_password = "ihqr ymgt cnpa oyul"
        if not smtp_password:
            smtp_password = SMTP_PASSWORD
            
        if not smtp_password:
            raise ValueError("SMTP password not configured")
        
        # Create SMTP client with standard library
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            logger.info("STARTTLS established")
            
            logger.info(f"Attempting login with {SMTP_USERNAME}")
            server.login(SMTP_USERNAME, smtp_password)
            logger.info("SMTP login successful")
            
            server.send_message(message)
            logger.info(f"Email sent successfully to {to_email}")
            
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        # Log more detailed error information
        import traceback
        logger.error(traceback.format_exc())
        return False

async def _send_email(to_email: str, subject: str, body: str):
    """Wrapper for sync email sending function to be called from async code"""
    # Use a thread to send email synchronously without blocking the event loop
    email_thread = threading.Thread(
        target=_send_email_sync,
        args=(to_email, subject, body)
    )
    email_thread.start()
    return True

async def send_prospect_email(lead: Lead):
    subject = "Lead Submission Confirmation"
    body = f"""
    Dear {lead.first_name} {lead.last_name},
    
    Your request was submitted to us. Thank you for your interest.
    
    Best regards,
    The Team
    """
    return await _send_email(lead.email, subject, body)

async def send_attorney_email(lead: Lead):
    subject = "New Lead Submission"
    body = f"""
    You have got a new lead
    
    Lead Details:
    - Name: {lead.first_name} {lead.last_name}
    - Email: {lead.email}
    """
    return await _send_email(ATTORNEY_EMAIL, subject, body)
