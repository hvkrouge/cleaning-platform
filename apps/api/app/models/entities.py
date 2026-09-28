from __future__ import annotations

from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    PARTNER = "PARTNER"
    OPERATIONS = "OPERATIONS"
    FINANCE = "FINANCE"
    SUPPORT = "SUPPORT"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class PartnerStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"


class ServicePricingType(str, Enum):
    PACKAGE = "PACKAGE"
    HOURLY = "HOURLY"
    SQFT = "SQFT"
    QUOTE = "QUOTE"


class BookingStatus(str, Enum):
    DRAFT = "DRAFT"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    CONFIRMED = "CONFIRMED"
    ASSIGNMENT_PENDING = "ASSIGNMENT_PENDING"
    PARTNER_ASSIGNED = "PARTNER_ASSIGNED"
    PARTNER_ACCEPTED = "PARTNER_ACCEPTED"
    EN_ROUTE = "EN_ROUTE"
    ARRIVED = "ARRIVED"
    IN_PROGRESS = "IN_PROGRESS"
    QUALITY_CHECK = "QUALITY_CHECK"
    COMPLETED = "COMPLETED"
    PAYOUT_PENDING = "PAYOUT_PENDING"
    SETTLED = "SETTLED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
    REASSIGNMENT_REQUIRED = "REASSIGNMENT_REQUIRED"
    DISPUTED = "DISPUTED"
    REFUND_PENDING = "REFUND_PENDING"
    REFUNDED = "REFUNDED"


class AssignmentStatus(str, Enum):
    OFFERED = "OFFERED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class JobStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class EarningStatus(str, Enum):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    PAID = "PAID"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.CUSTOMER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped[User] = relationship()
    properties: Mapped[list[Property]] = relationship(back_populates="customer", cascade="all, delete-orphan")


class Partner(Base):
    __tablename__ = "partners"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    status: Mapped[PartnerStatus] = mapped_column(SAEnum(PartnerStatus), default=PartnerStatus.PENDING)
    rating: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=5.00)
    total_jobs: Mapped[int] = mapped_column(Integer, default=0)
    user: Mapped[User] = relationship()
    availability: Mapped[list[PartnerAvailability]] = relationship(back_populates="partner", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    line1: Mapped[str] = mapped_column(String(255))
    area: Mapped[str] = mapped_column(String(120), index=True)
    city: Mapped[str] = mapped_column(String(120), default="Bengaluru")
    state: Mapped[str] = mapped_column(String(120), default="Karnataka")
    pincode: Mapped[str] = mapped_column(String(10))


class Property(Base):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    name: Mapped[str] = mapped_column(String(120))
    property_type: Mapped[str] = mapped_column(String(50), default="APARTMENT")
    bhk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sqft: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[int] = mapped_column(Integer, default=1)
    balconies: Mapped[int] = mapped_column(Integer, default=0)
    furnished: Mapped[bool] = mapped_column(Boolean, default=False)
    customer: Mapped[Customer] = relationship(back_populates="properties")
    address: Mapped[Address] = relationship()


class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(50), default="HOME")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pricing_type: Mapped[ServicePricingType] = mapped_column(SAEnum(ServicePricingType), default=ServicePricingType.PACKAGE)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    packages: Mapped[list[ServicePackage]] = relationship(back_populates="service", cascade="all, delete-orphan")
    addons: Mapped[list[ServiceAddon]] = relationship(back_populates="service", cascade="all, delete-orphan")


class ServicePackage(Base):
    __tablename__ = "service_packages"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    name: Mapped[str] = mapped_column(String(120))
    min_bhk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    max_bhk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    estimated_minutes: Mapped[int] = mapped_column(Integer)
    required_workers: Mapped[int] = mapped_column(Integer, default=1)
    service: Mapped[Service] = relationship(back_populates="packages")


class ServiceAddon(Base):
    __tablename__ = "service_addons"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    name: Mapped[str] = mapped_column(String(120))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=30)
    service: Mapped[Service] = relationship(back_populates="addons")


class PartnerAvailability(Base):
    __tablename__ = "partner_availability"
    id: Mapped[int] = mapped_column(primary_key=True)
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))
    date: Mapped[date] = mapped_column(Date)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    status: Mapped[str] = mapped_column(String(20), default="AVAILABLE")
    partner: Mapped[Partner] = relationship(back_populates="availability")


class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_number: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    package_id: Mapped[Optional[int]] = mapped_column(ForeignKey("service_packages.id"), nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    required_workers: Mapped[int] = mapped_column(Integer)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    discount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    tax: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[BookingStatus] = mapped_column(SAEnum(BookingStatus), default=BookingStatus.CONFIRMED)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BookingItem(Base):
    __tablename__ = "booking_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    item_type: Mapped[str] = mapped_column(String(30))
    item_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(120))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2))


class BookingStatusHistory(Base):
    __tablename__ = "booking_status_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    old_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    new_status: Mapped[str] = mapped_column(String(50))
    changed_by_user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class BookingAssignment(Base):
    __tablename__ = "booking_assignments"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))
    status: Mapped[AssignmentStatus] = mapped_column(SAEnum(AssignmentStatus), default=AssignmentStatus.OFFERED)
    offered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), unique=True)
    lead_partner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("partners.id"), nullable=True)
    status: Mapped[JobStatus] = mapped_column(SAEnum(JobStatus), default=JobStatus.NOT_STARTED)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    actual_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class JobChecklist(Base):
    __tablename__ = "job_checklists"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    section: Mapped[str] = mapped_column(String(80))
    item: Mapped[str] = mapped_column(String(160))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)


class JobMedia(Base):
    __tablename__ = "job_media"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    media_type: Mapped[str] = mapped_column(String(20))
    file_url: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[PaymentStatus] = mapped_column(SAEnum(PaymentStatus), default=PaymentStatus.PENDING)
    gateway: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    gateway_transaction_id: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class PartnerEarning(Base):
    __tablename__ = "partner_earnings"
    id: Mapped[int] = mapped_column(primary_key=True)
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    earning_type: Mapped[str] = mapped_column(String(40), default="JOB_PAYOUT")
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[EarningStatus] = mapped_column(SAEnum(EarningStatus), default=EarningStatus.AVAILABLE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
