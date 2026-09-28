from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db import Base, engine
from app.routers import services, customers, bookings, partners, admin

Base.metadata.create_all(engine)

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(services.router)
app.include_router(customers.router)
app.include_router(bookings.router)
app.include_router(partners.router)
app.include_router(admin.router)

@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}
