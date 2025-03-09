"""
This file deals with the schema for the request and response by the client and api

"""

from pydantic import BaseModel, EmailStr
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
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    UID: int
    email: str
    password: str
    time_created: datetime


    class Config:
        from_attributes = True