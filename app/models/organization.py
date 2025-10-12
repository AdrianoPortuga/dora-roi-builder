from sqlalchemy import Column, Integer, String
from .base import Base

class Organization(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
