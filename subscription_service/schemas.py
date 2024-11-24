""" 
    Pydantic models (new file for request/response validation)

"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class SubscriptionCreate(BaseModel):
    email: EmailStr


class SubscriptionResponse(BaseModel):
    id: int
    email: EmailStr
    start_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        form_attribute = True  # Enables automatic conversion from SQLAlchemy objects
