from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.entities import Booking, BookingStatus, Payment, PaymentStatus, Partner, BookingAssignment, AssignmentStatus, Job
from app.schemas.core import BookingCreate, BookingOut, QuoteRequest, QuoteOut, AssignBookingRequest
from app.services.booking import calculate_quote, create_booking, record_status

router = APIRouter(tags=["bookings"])

@router.post("/pricing/quote", response_model=QuoteOut)
def quote(payload: QuoteRequest, db: Session = Depends(get_db)):
    try:
        result = calculate_quote(db, payload)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    result.pop("package")
    return result

@router.post("/bookings", response_model=BookingOut)
def create(payload: BookingCreate, db: Session = Depends(get_db)):
    try:
        booking, _ = create_booking(db, payload)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    # MVP: simulate successful payment; swap with gateway callback later.
    db.add(Payment(booking_id=booking.id, amount=booking.total, status=PaymentStatus.SUCCESS, gateway="mock", gateway_transaction_id=f"mock_{booking.id}"))
    record_status(db, booking, BookingStatus.ASSIGNMENT_PENDING)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/bookings")
def list_bookings(db: Session = Depends(get_db)):
    return db.scalars(select(Booking).order_by(Booking.created_at.desc())).all()

@router.get("/bookings/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking

@router.post("/admin/bookings/{booking_id}/assign")
def assign(booking_id: int, payload: AssignBookingRequest, db: Session = Depends(get_db)):
    booking = db.get(Booking, booking_id)
    partner = db.get(Partner, payload.partner_id)
    if not booking or not partner:
        raise HTTPException(404, "Booking or partner not found")
    if partner.status.value != "VERIFIED":
        raise HTTPException(400, "Partner is not verified")
    assignment = BookingAssignment(booking_id=booking.id, partner_id=partner.id, status=AssignmentStatus.OFFERED)
    db.add(assignment)
    record_status(db, booking, BookingStatus.PARTNER_ASSIGNED)
    db.commit()
    db.refresh(assignment)
    return {"assignment_id": assignment.id, "status": assignment.status}
