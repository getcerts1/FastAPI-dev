"""
This file deals with the schema for the request and response by the client and api

"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PostRequest(BaseModel):
    title:str
    content:str
    rating: Optional[int] = None


class PostResponse(BaseModel):
    PID:int
    title:str
    content:str
    rating: Optional[int] = None
    time_created: datetime

    class Config:
        from_attributes = True


class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None  # Nullable email with proper validation

class UserResponse(BaseModel):
    UID: int
    first_name: str
    last_name: str
    email: Optional[str] = None  # Nullable email with proper validation
    time_created: datetime


    class Config:
        from_attributes = True