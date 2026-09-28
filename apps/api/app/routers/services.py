from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.entities import Service
from app.schemas.core import ServiceOut

router = APIRouter(prefix="/services", tags=["services"])

@router.get("", response_model=list[ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.scalars(select(Service).where(Service.active.is_(True)).order_by(Service.id)).all()

@router.get("/{service_id}")
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(404, "Service not found")
    return {
        "id": service.id,
        "name": service.name,
        "category": service.category,
        "pricing_type": service.pricing_type,
        "packages": service.packages,
        "addons": service.addons,
    }
