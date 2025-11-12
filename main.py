import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Appointment, ContactMessage

app = FastAPI(title="HMS Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "HMS Backend running"}

@app.get("/test")
def test_database():
    ok = db is not None
    return {
        "backend": "✅ Running",
        "database": "✅ Connected" if ok else "❌ Not Connected",
        "database_name": getattr(db, 'name', None)
    }

# ----- Reference data (static for landing page display) -----
SERVICES = [
    {"title": "Emergency Care", "description": "24/7 critical care with rapid response.", "icon": "Activity"},
    {"title": "Surgery", "description": "Advanced surgical procedures by experts.", "icon": "Scalpel"},
    {"title": "Diagnostics", "description": "Modern imaging and lab diagnostics.", "icon": "ScanLine"},
    {"title": "Pharmacy", "description": "On-site pharmacy with verified medicines.", "icon": "Pill"},
]

DEPARTMENTS = [
    {"name": "Cardiology", "description": "Heart and vascular care."},
    {"name": "Neurology", "description": "Brain and nervous system."},
    {"name": "Pediatrics", "description": "Child health and wellness."},
    {"name": "Orthopedics", "description": "Bones and joints."},
    {"name": "Oncology", "description": "Cancer care."},
    {"name": "Dermatology", "description": "Skin care."},
]

DOCTORS = [
    {"name": "Dr. Sarah Johnson", "specialization": "Cardiologist", "photo": "https://images.unsplash.com/photo-1550831107-1553da8c8464?w=640&q=80"},
    {"name": "Dr. Amit Verma", "specialization": "Neurologist", "photo": "https://images.unsplash.com/photo-1606813907291-76b6619b8e0e?w=640&q=80"},
    {"name": "Dr. Emily Chen", "specialization": "Pediatrician", "photo": "https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=640&q=80"},
    {"name": "Dr. Lucas Brown", "specialization": "Orthopedic Surgeon", "photo": "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=640&q=80"},
]

@app.get("/api/services")
def list_services():
    return SERVICES

@app.get("/api/departments")
def list_departments():
    return DEPARTMENTS

@app.get("/api/doctors")
def list_doctors():
    return DOCTORS

# ----- Form submissions: persist to MongoDB -----
@app.post("/api/appointment")
def create_appointment(payload: Appointment):
    try:
        inserted_id = create_document("appointment", payload)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def create_contact(payload: ContactMessage):
    try:
        inserted_id = create_document("contactmessage", payload)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
