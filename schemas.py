from pydantic import BaseModel
from datetime import datetime
from typing import List

class LeadSchema(BaseModel):
    name: str
    signal: List[int]

class ECGSchema(BaseModel):
    id: int
    date: datetime
    leads: List[LeadSchema]

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        orm_mode = True
        