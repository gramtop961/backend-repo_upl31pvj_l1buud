"""
Database Schemas for Hospital Management System (HMS)

Each Pydantic model below represents a MongoDB collection. The collection
name is the lowercase version of the class name (e.g., Appointment -> "appointment").
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class Appointment(BaseModel):
    """Appointment booking requests from the landing page"""
    name: str = Field(..., description="Patient full name")
    email: EmailStr = Field(..., description="Patient email")
    phone: str = Field(..., description="Patient phone number")
    department: str = Field(..., description="Requested department")
    doctor: Optional[str] = Field(None, description="Requested doctor (optional)")
    message: Optional[str] = Field(None, description="Brief note or symptoms")

class ContactMessage(BaseModel):
    """General contact form submissions"""
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    phone: Optional[str] = Field(None, description="Sender phone")
    message: str = Field(..., description="Message body")

# Optional reference data models (served from code/static for landing page)
class Doctor(BaseModel):
    name: str
    specialization: str
    photo: str

class Service(BaseModel):
    title: str
    description: str
    icon: str

class Department(BaseModel):
    name: str
    description: str
