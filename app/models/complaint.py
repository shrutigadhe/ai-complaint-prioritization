from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from datetime import datetime
from app.database.connections import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    complaint_text = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    department = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    requires_human_review = Column(Boolean, default=False)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)
