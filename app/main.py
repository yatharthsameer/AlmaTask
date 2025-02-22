import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from fastapi import FastAPI, File, Form, HTTPException, Depends, UploadFile, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from typing import List, Optional
import os
from uuid import UUID, uuid4

from .auth import create_access_token, get_current_user
from .models import Lead, LeadStatus
from .schemas import LeadCreate, LeadUpdate, LeadResponse
from .database import db
from .email_service import send_prospect_email, send_attorney_email
from .config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Ensure upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # For MVP, we'll use a simple hardcoded check
    if form_data.username == "attorney" and form_data.password == "password":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.post("/api/leads", status_code=status.HTTP_201_CREATED)
async def create_lead(
    background_tasks: BackgroundTasks,  # Inject as parameter
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = File(...),
):
    # Validate file extension
    file_ext = os.path.splitext(resume.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension not allowed. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Save resume file
    file_id = uuid4()
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    try:
        contents = await resume.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB"
            )
        
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save file"
        )

    # Create lead
    lead = Lead(
        first_name=first_name,
        last_name=last_name,
        email=email,
        resume_path=str(file_path)
    )
    db.create_lead(lead)

    # Add email tasks to background tasks
    background_tasks.add_task(send_prospect_email, lead)
    background_tasks.add_task(send_attorney_email, lead)

    return {"id": lead.id}

@app.get("/api/leads", response_model=List[LeadResponse])
async def get_leads(
    status: Optional[LeadStatus] = None,
    current_user: str = Depends(get_current_user)
):
    if status:
        return db.get_leads_by_status(status)
    return db.get_all_leads()

@app.get("/api/leads/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: UUID,
    current_user: str = Depends(get_current_user)
):
    if lead := db.get_lead(lead_id):
        return lead
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Lead not found"
    )

@app.patch("/api/leads/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: UUID,
    lead_update: LeadUpdate,
    current_user: str = Depends(get_current_user)
):
    if updated_lead := db.update_lead(lead_id, lead_update.status, lead_update.notes):
        return updated_lead
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Lead not found"
    )

@app.get("/api/leads/files/{lead_id}")
async def get_resume(
    lead_id: UUID,
    current_user: str = Depends(get_current_user)
):
    if lead := db.get_lead(lead_id):
        if os.path.exists(lead.resume_path):
            return FileResponse(lead.resume_path)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Lead not found"
    )
    
@app.post("/api/test/email")
async def test_email(background_tasks: BackgroundTasks):
    """Test endpoint to verify email sending"""
    test_lead = Lead(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        resume_path="test_path"
    )
    
    # Add email tasks to background tasks
    background_tasks.add_task(send_prospect_email, test_lead)
    background_tasks.add_task(send_attorney_email, test_lead)
    
    return {"message": "Test emails triggered"}
