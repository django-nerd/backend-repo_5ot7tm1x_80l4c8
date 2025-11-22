"""
Database Schemas for Vector Strength Gym

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercased class name (e.g., Booking -> "booking").
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class Booking(BaseModel):
    full_name: str = Field(..., description="Member full name")
    email: EmailStr
    phone: Optional[str] = Field(None, description="Phone number")
    class_type: str = Field(..., description="Class type or facility booking")
    date: str = Field(..., description="ISO date string YYYY-MM-DD")
    time: str = Field(..., description="Time string, e.g., 18:00")
    notes: Optional[str] = Field(None, description="Additional notes")


class Admission(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    plan: str = Field(..., description="Membership plan: Monthly/Quarterly/Yearly")
    objectives: Optional[str] = None


class TrainerApplication(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    experience_years: Optional[int] = Field(None, ge=0, le=60)
    specialties: Optional[str] = Field(None, description="Comma-separated specialties")
    bio: Optional[str] = None


class Review(BaseModel):
    full_name: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    created_at: Optional[datetime] = None


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to the assistant")


class ChatResponse(BaseModel):
    reply: str


class ClassBooking(BaseModel):
    full_name: str
    email: EmailStr
    class_type: str
    date: str
    time: str


class ClassJoin(BaseModel):
    full_name: str
    email: EmailStr
    class_code: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    ok: bool
    token: Optional[str] = None
    detail: Optional[str] = None
