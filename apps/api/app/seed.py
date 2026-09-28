from datetime import date, datetime, time, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Base, engine, SessionLocal
from app.models.entities import *


def seed():
    Base.metadata.create_all(engine)
    db: Session = SessionLocal()
    try:
        if db.scalar(select(Service).limit(1)):
            return
        customer_user = User(name="Demo Customer", phone="9999999991", email="demo@example.com", role=UserRole.CUSTOMER)
        partner_user = User(name="Demo Partner", phone="9999999992", email="partner@example.com", role=UserRole.PARTNER)
        admin_user = User(name="Demo Operations", phone="9999999993", email="ops@example.com", role=UserRole.OPERATIONS)
        db.add_all([customer_user, partner_user, admin_user]); db.flush()
        customer = Customer(user_id=customer_user.id)
        partner = Partner(user_id=partner_user.id, status=PartnerStatus.VERIFIED, rating=Decimal("4.80"))
        db.add_all([customer, partner]); db.flush()

        addr = Address(line1="Demo Apartment, Whitefield", area="Whitefield", city="Bengaluru", state="Karnataka", pincode="560066")
        db.add(addr); db.flush()
        prop = Property(customer_id=customer.id, address_id=addr.id, name="Demo Home", property_type="APARTMENT", bhk=2, sqft=1050, bathrooms=2, balconies=1, furnished=True)
        db.add(prop)

        svc = Service(name="Deep Cleaning", category="HOME", pricing_type=ServicePricingType.PACKAGE, active=True, description="Whole-home deep cleaning")
        db.add(svc); db.flush()
        packages = [
            ServicePackage(service_id=svc.id, name="1 BHK Deep Cleaning", min_bhk=1, max_bhk=1, base_price=2499, estimated_minutes=180, required_workers=2),
            ServicePackage(service_id=svc.id, name="2 BHK Deep Cleaning", min_bhk=2, max_bhk=2, base_price=3499, estimated_minutes=240, required_workers=2),
            ServicePackage(service_id=svc.id, name="3 BHK Deep Cleaning", min_bhk=3, max_bhk=3, base_price=4499, estimated_minutes=300, required_workers=2),
        ]
        db.add_all(packages)
        db.add_all([
            ServiceAddon(service_id=svc.id, name="Kitchen Deep Clean", price=799, estimated_minutes=45),
            ServiceAddon(service_id=svc.id, name="Sofa Cleaning", price=699, estimated_minutes=45),
            ServiceAddon(service_id=svc.id, name="Balcony Cleaning", price=299, estimated_minutes=20),
        ])
        tomorrow = date.today() + timedelta(days=1)
        db.add(PartnerAvailability(partner_id=partner.id, date=tomorrow, start_time=time(9), end_time=time(18), status="AVAILABLE"))
        db.commit()
        print("Seeded demo data")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
