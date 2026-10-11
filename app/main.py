from fastapi import FastAPI

from app.database.connections import Base, engine
from app.api.complaints import router as complaint_router
from app.api.auth import router as auth_router
from app.api.analytics import router as analytics_router

from app.models.complaint import Complaint
from app.models.user import User
from app.models.history import ComplaintHistory

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Emergency Complaint Prioritization API",
    version="1.0.0"
)

app.include_router(complaint_router)
app.include_router(complaint_router)
app.include_router(analytics_router)



@app.get("/")
def home():

    return {
        "message": "AI Complaint Prioritization API is running"
    }