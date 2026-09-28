from datetime import datetime
from uuid import uuid4
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import (
    Booking, BookingItem, BookingStatus, BookingStatusHistory,
    Service, ServiceAddon, ServicePackage, Property
)
from app.schemas.core import QuoteRequest


def calculate_quote(db: Session, request: QuoteRequest):
    service = db.get(Service, request.service_id)
    prop = db.get(Property, request.property_id)
    if not service or not prop or not service.active:
        raise ValueError("Invalid service or property")

    package = None
    if prop.bhk is not None:
        package = db.scalar(
            select(ServicePackage).where(
                ServicePackage.service_id == service.id,
                ((ServicePackage.min_bhk.is_(None)) | (ServicePackage.min_bhk <= prop.bhk)),
                ((ServicePackage.max_bhk.is_(None)) | (ServicePackage.max_bhk >= prop.bhk)),
            ).order_by(ServicePackage.base_price)
        )
    else:
        package = db.scalar(select(ServicePackage).where(ServicePackage.service_id == service.id).order_by(ServicePackage.base_price))
    if not package:
        raise ValueError("No package configured for this property")

    addon_total = Decimal("0")
    addon_minutes = 0
    if request.addon_ids:
        addons = db.scalars(select(ServiceAddon).where(ServiceAddon.id.in_(request.addon_ids), ServiceAddon.service_id == service.id)).all()
        for addon in addons:
            addon_total += Decimal(addon.price)
            addon_minutes += addon.estimated_minutes

    surcharge = Decimal("0")
    if prop.sqft and prop.sqft > 1200:
        surcharge += Decimal("300")
    if prop.sqft and prop.sqft > 1500:
        surcharge += Decimal("500")
    if prop.furnished:
        surcharge += Decimal("200")

    base = Decimal(package.base_price)
    total = base + addon_total + surcharge
    duration = package.estimated_minutes + addon_minutes
    return {
        "base_price": base,
        "addons_total": addon_total,
        "surcharge": surcharge,
        "discount": Decimal("0"),
        "tax": Decimal("0"),
        "total": total,
        "estimated_duration_minutes": duration,
        "required_workers": package.required_workers,
        "package": package,
    }


def record_status(db: Session, booking: Booking, new_status: BookingStatus, changed_by_user_id=None, reason=None):
    old = booking.status.value if booking.status else None
    booking.status = new_status
    db.add(BookingStatusHistory(
        booking_id=booking.id,
        old_status=old,
        new_status=new_status.value,
        changed_by_user_id=changed_by_user_id,
        reason=reason,
    ))


def create_booking(db: Session, request):
    quote = calculate_quote(db, QuoteRequest(
        service_id=request.service_id,
        property_id=request.property_id,
        addon_ids=request.addon_ids,
        scheduled_at=request.scheduled_at,
    ))
    booking = Booking(
        booking_number=f"CLN-{datetime.utcnow():%Y%m%d}-{uuid4().hex[:8].upper()}",
        customer_id=request.customer_id,
        property_id=request.property_id,
        service_id=request.service_id,
        package_id=quote["package"].id,
        scheduled_at=request.scheduled_at,
        duration_minutes=quote["estimated_duration_minutes"],
        required_workers=quote["required_workers"],
        subtotal=quote["base_price"] + quote["addons_total"] + quote["surcharge"],
        discount=quote["discount"],
        tax=quote["tax"],
        total=quote["total"],
        status=BookingStatus.CONFIRMED,
    )
    db.add(booking)
    db.flush()
    db.add(BookingStatusHistory(booking_id=booking.id, old_status=None, new_status=BookingStatus.CONFIRMED.value))
    for addon_id in request.addon_ids:
        addon = db.get(ServiceAddon, addon_id)
        if addon:
            db.add(BookingItem(
                booking_id=booking.id, item_type="ADDON", item_id=addon.id,
                name=addon.name, quantity=1, unit_price=addon.price, total=addon.price,
            ))
    db.commit()
    db.refresh(booking)
    return booking, quote
