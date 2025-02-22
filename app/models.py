from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

class LeadStatus(str, Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class Lead:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        resume_path: str,
        id: UUID = None,
        status: LeadStatus = LeadStatus.PENDING,
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.resume_path = resume_path
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update_status(self, status: LeadStatus, notes: Optional[str] = None):
        self.status = status
        if notes:
            self.notes = notes
        self.updated_at = datetime.utcnow()
