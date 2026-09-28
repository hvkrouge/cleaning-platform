from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.entities import Booking, BookingStatus, Partner

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    bookings = db.scalar(select(func.count()).select_from(Booking)) or 0
    revenue = db.scalar(select(func.coalesce(func.sum(Booking.total), 0)).where(Booking.status.notin_([BookingStatus.CANCELLED, BookingStatus.REFUNDED]))) or 0
    active_partners = db.scalar(select(func.count()).select_from(Partner).where(Partner.status == "VERIFIED")) or 0
    unassigned = db.scalar(select(func.count()).select_from(Booking).where(Booking.status == BookingStatus.ASSIGNMENT_PENDING)) or 0
    return {
        "bookings": bookings,
        "revenue": revenue,
        "verified_partners": active_partners,
        "unassigned_bookings": unassigned,
    }
