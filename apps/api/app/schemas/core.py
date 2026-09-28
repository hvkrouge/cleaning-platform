from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.entities import BookingStatus


class AddressCreate(BaseModel):
    line1: str
    area: str
    city: str = "Bengaluru"
    state: str = "Karnataka"
    pincode: str


class PropertyCreate(BaseModel):
    customer_id: int
    address: AddressCreate
    name: str
    property_type: str = "APARTMENT"
    bhk: Optional[int] = None
    sqft: Optional[int] = None
    bathrooms: int = 1
    balconies: int = 0
    furnished: bool = False


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: str
    pricing_type: str


class PackageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    base_price: Decimal
    estimated_minutes: int
    required_workers: int


class AddonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: Decimal
    estimated_minutes: int


class QuoteRequest(BaseModel):
    service_id: int
    property_id: int
    addon_ids: list[int] = Field(default_factory=list)
    scheduled_at: datetime


class QuoteOut(BaseModel):
    base_price: Decimal
    addons_total: Decimal
    surcharge: Decimal
    discount: Decimal = Decimal("0")
    tax: Decimal = Decimal("0")
    total: Decimal
    estimated_duration_minutes: int
    required_workers: int


class BookingCreate(BaseModel):
    customer_id: int
    property_id: int
    service_id: int
    package_id: Optional[int] = None
    addon_ids: list[int] = Field(default_factory=list)
    scheduled_at: datetime


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    booking_number: str
    status: BookingStatus
    scheduled_at: datetime
    duration_minutes: int
    required_workers: int
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal


class AvailabilityCreate(BaseModel):
    partner_id: int
    date: date
    start_time: time
    end_time: time


class AssignBookingRequest(BaseModel):
    partner_id: int


class PartnerJobAction(BaseModel):
    reason: Optional[str] = None


class ReviewCreate(BaseModel):
    booking_id: int
    rating: int = Field(ge=1, le=5)
    punctuality: Optional[int] = Field(default=None, ge=1, le=5)
    quality: Optional[int] = Field(default=None, ge=1, le=5)
    professionalism: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None
