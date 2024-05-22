from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class LeadState(str, Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    resume: Optional[str] = None

class LeadUpdate(BaseModel):
    state: LeadState

class Lead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    resume: Optional[str] = None
    state: str

    class Config:
        orm_mode = True
