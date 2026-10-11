from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connections import get_db
from app.models.complaint import Complaint

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total = db.query(Complaint).count()
    open_count = db.query(Complaint).filter(Complaint.status == "OPEN").count()
    resolved = db.query(Complaint).filter(Complaint.status == "RESOLVED").count()
    critical = db.query(Complaint).filter(Complaint.priority == "CRITICAL").count()
    human_review = db.query(Complaint).filter(Complaint.requires_human_review == True).count()

    return {
        "total_complaints": total,
        "open": open_count,
        "resolved": resolved,
        "critical": critical,
        "requires_human_review": human_review
    }


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    results = db.query(
        Complaint.category, func.count(Complaint.id)
    ).group_by(Complaint.category).all()

    return [{"category": cat, "count": count} for cat, count in results]


@router.get("/priorities")
def get_priorities(db: Session = Depends(get_db)):
    results = db.query(
        Complaint.priority, func.count(Complaint.id)
    ).group_by(Complaint.priority).all()

    return [{"priority": pri, "count": count} for pri, count in results]


@router.get("/departments")
def get_departments(db: Session = Depends(get_db)):
    results = db.query(
        Complaint.department, func.count(Complaint.id)
    ).group_by(Complaint.department).all()

    return [{"department": dept, "count": count} for dept, count in results]
