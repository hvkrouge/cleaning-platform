from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.entities import Partner, BookingAssignment, AssignmentStatus, Booking, BookingStatus, Job, JobStatus, PartnerEarning, EarningStatus
from app.schemas.core import AvailabilityCreate
from app.services.booking import record_status

router = APIRouter(prefix="/partners", tags=["partners"])

@router.post("/availability")
def set_availability(payload: AvailabilityCreate, db: Session = Depends(get_db)):
    partner = db.get(Partner, payload.partner_id)
    if not partner:
        raise HTTPException(404, "Partner not found")
    from app.models.entities import PartnerAvailability
    item = PartnerAvailability(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{partner_id}/jobs")
def jobs(partner_id: int, db: Session = Depends(get_db)):
    return db.execute(
        select(BookingAssignment, Booking)
        .join(Booking, Booking.id == BookingAssignment.booking_id)
        .where(BookingAssignment.partner_id == partner_id)
        .order_by(Booking.scheduled_at)
    ).all()

@router.post("/{partner_id}/assignments/{assignment_id}/accept")
def accept(partner_id: int, assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.get(BookingAssignment, assignment_id)
    if not assignment or assignment.partner_id != partner_id:
        raise HTTPException(404, "Assignment not found")
    booking = db.get(Booking, assignment.booking_id)
    assignment.status = AssignmentStatus.ACCEPTED
    assignment.accepted_at = datetime.utcnow()
    record_status(db, booking, BookingStatus.PARTNER_ACCEPTED)
    job = Job(booking_id=booking.id, lead_partner_id=partner_id, status=JobStatus.NOT_STARTED)
    db.add(job)
    db.commit()
    return {"booking_id": booking.id, "status": assignment.status}

@router.post("/{partner_id}/bookings/{booking_id}/start")
def start_job(partner_id: int, booking_id: int, db: Session = Depends(get_db)):
    job = db.scalar(select(Job).where(Job.booking_id == booking_id, Job.lead_partner_id == partner_id))
    booking = db.get(Booking, booking_id)
    if not job or not booking:
        raise HTTPException(404, "Job not found")
    job.status = JobStatus.IN_PROGRESS
    job.started_at = datetime.utcnow()
    record_status(db, booking, BookingStatus.IN_PROGRESS)
    db.commit()
    return {"status": job.status}

@router.post("/{partner_id}/bookings/{booking_id}/complete")
def complete_job(partner_id: int, booking_id: int, db: Session = Depends(get_db)):
    job = db.scalar(select(Job).where(Job.booking_id == booking_id, Job.lead_partner_id == partner_id))
    booking = db.get(Booking, booking_id)
    if not job or not booking:
        raise HTTPException(404, "Job not found")
    job.status = JobStatus.COMPLETED
    job.completed_at = datetime.utcnow()
    if job.started_at:
        job.actual_duration_minutes = max(1, int((job.completed_at - job.started_at).total_seconds() / 60))
    record_status(db, booking, BookingStatus.COMPLETED)
    record_status(db, booking, BookingStatus.PAYOUT_PENDING)
    # MVP payout: 60% of booking total.
    payout = booking.total * Decimal("0.60")
    db.add(PartnerEarning(partner_id=partner_id, booking_id=booking.id, amount=payout, status=EarningStatus.AVAILABLE))
    partner = db.get(Partner, partner_id)
    partner.total_jobs += 1
    db.commit()
    return {"status": job.status, "partner_payout": payout}
