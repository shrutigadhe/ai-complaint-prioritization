from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connections import get_db
from app.models.complaint import Complaint
from app.schemas.complaint import ComplaintCreate, ComplaintResponse
from app.services.classifier import predict_complaint

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)

@router.post("/", response_model=ComplaintResponse)
def create_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db)
):
    # Run AI Classification & Priority Prediction
    prediction = predict_complaint(complaint.complaint_text)

    new_complaint = Complaint(
        complaint_text=complaint.complaint_text,
        category=prediction["category"],
        priority=prediction["priority"],
        department=prediction["department"],
        confidence=prediction["confidence"],
        requires_human_review=prediction["requires_human_review"]
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return new_complaint

@router.get("/", response_model=list[ComplaintResponse])
def get_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).all()

@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@router.delete("/{complaint_id}")
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()

    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    db.delete(complaint)
    db.commit()

    return {
        "message": f"Complaint {complaint_id}  deleted successfully",
        "complaint_id": complaint_id
    }

@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(complaint_id: int, status: str, db: Session = Depends(get_db)):
    from app.models.history import ComplaintHistory
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    history = ComplaintHistory(
        complaint_id=complaint.id,
        old_status=complaint.status,
        new_status=status,
        changed_by="system"
    )
    db.add(history)
    complaint.status = status
    db.commit()
    db.refresh(complaint)
    return complaint