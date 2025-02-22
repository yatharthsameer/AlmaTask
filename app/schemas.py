from enum import Enum
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

class LeadStatus(str, Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None
    notes: Optional[str] = None

class LeadResponse(LeadBase):
    id: UUID
    resume_path: str
    status: LeadStatus
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True
