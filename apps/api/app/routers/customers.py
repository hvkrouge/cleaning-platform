from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.entities import Address, Property
from app.schemas.core import PropertyCreate

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/properties")
def create_property(payload: PropertyCreate, db: Session = Depends(get_db)):
    address = Address(**payload.address.model_dump())
    db.add(address)
    db.flush()
    prop = Property(
        customer_id=payload.customer_id,
        address_id=address.id,
        name=payload.name,
        property_type=payload.property_type,
        bhk=payload.bhk,
        sqft=payload.sqft,
        bathrooms=payload.bathrooms,
        balconies=payload.balconies,
        furnished=payload.furnished,
    )
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop

@router.get("/{customer_id}/properties")
def list_properties(customer_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(Property).where(Property.customer_id == customer_id)).all()
