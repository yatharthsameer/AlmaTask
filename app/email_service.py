import logging
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from .models import Lead
from fastapi.background import BackgroundTasks

logger = logging.getLogger(__name__)

# Email configuration
ATTORNEY_EMAIL = os.getenv("ATTORNEY_EMAIL", "thesameerbros@gmail.com")
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "ytharthsmr@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

async def _send_email(to_email: str, subject: str, body: str):
    try:
        message = MIMEMultipart()
        message["From"] = SMTP_USERNAME
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        async with SMTP(hostname=SMTP_SERVER, port=SMTP_PORT, use_tls=False) as smtp:
            await smtp.starttls()
            await smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            await smtp.send_message(message)
            
        logger.info(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

async def send_prospect_email(background_tasks: BackgroundTasks, lead: Lead):
    subject = "Lead Submission Confirmation"
    body = f"""
    Dear {lead.first_name} {lead.last_name},
    
    Your request was submitted to us. Thank you for your interest.
    
    Best regards,
    The Team
    """
    background_tasks.add_task(_send_email, lead.email, subject, body)

async def send_attorney_email(background_tasks: BackgroundTasks, lead: Lead):
    subject = "New Lead Submission"
    body = f"""
    You have got a new lead
    
    Lead Details:
    - Name: {lead.first_name} {lead.last_name}
    - Email: {lead.email}
    """
    background_tasks.add_task(_send_email, ATTORNEY_EMAIL, subject, body)
