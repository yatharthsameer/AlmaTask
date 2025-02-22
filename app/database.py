from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from .models import Lead, LeadStatus

class InMemoryDB:
    def __init__(self):
        self.leads: Dict[UUID, Lead] = {}

    def create_lead(self, lead: Lead) -> Lead:
        """Create a new lead entry"""
        self.leads[lead.id] = lead
        return lead

    def get_lead(self, lead_id: UUID) -> Optional[Lead]:
        """Get a lead by ID"""
        return self.leads.get(lead_id)

    def get_all_leads(self) -> List[Lead]:
        """Get all leads, sorted by creation date (newest first)"""
        leads = list(self.leads.values())
        return sorted(leads, key=lambda x: x.created_at, reverse=True)

    def get_leads_by_status(self, status: LeadStatus) -> List[Lead]:
        """Get leads filtered by status, sorted by creation date (newest first)"""
        leads = [lead for lead in self.leads.values() if lead.status == status]
        return sorted(leads, key=lambda x: x.created_at, reverse=True)

    def update_lead(self, lead_id: UUID, status: LeadStatus, notes: Optional[str] = None) -> Optional[Lead]:
        """Update lead status and notes"""
        if lead := self.leads.get(lead_id):
            lead.update_status(status, notes)
            return lead
        return None

    def clear(self) -> None:
        """Clear all leads (useful for testing)"""
        self.leads.clear()

# Global database instance
db = InMemoryDB()
