from sqlalchemy import Column, Integer, String
from .base import Base

class Vendor(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, index=True)
    country = Column(String(5), nullable=True)
    criticality = Column(String(20), nullable=True)
