from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, DateTime, func

class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()
    created_at = Column(DateTime(timezone=True), server_default=func.now())
