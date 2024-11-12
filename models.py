from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class ECG(Base):
    __tablename__ = "ecgs"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    leads = relationship("Lead", back_populates="ecg")

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    ecg_id = Column(Integer, ForeignKey("ecgs.id"))
    name = Column(String)
    signal = Column(JSON)
    ecg = relationship("ECG", back_populates="leads")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    