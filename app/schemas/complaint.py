from pydantic import BaseModel
from typing import Optional

class ComplaintCreate(BaseModel):
    complaint_text: str

class ComplaintResponse(BaseModel):
    id: int
    complaint_text: str
    category: Optional[str] = None
    priority: Optional[str] = None
    department: Optional[str] = None
    confidence: Optional[float] = None
    requires_human_review: Optional[bool] = False
    status: str

    class Config:
        from_attributes = True
