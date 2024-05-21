from pydantic import BaseModel, EmailStr
from enum import Enum

class LeadState(str, Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    resume: str

class LeadUpdate(BaseModel):
    state: LeadState

class Lead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    resume: str
    state: LeadState

    class Config:
        orm_mode = True
