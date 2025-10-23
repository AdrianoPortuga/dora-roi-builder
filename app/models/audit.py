from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.models.base import Base

class AuditLog(Base):
    __tablename__ = "auditlog"

    id = Column(Integer, primary_key=True, index=True)
    # timestamps
    ts_utc = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # request / user context
    user_id = Column(Integer, nullable=True)
    user_email = Column(String(255), nullable=True)

    method = Column(String(16), nullable=False)
    path = Column(String(512), nullable=False)
    query = Column(Text, nullable=True)

    status_code = Column(Integer, nullable=False)
    latency_ms = Column(Integer, nullable=False)

    ip = Column(String(64), nullable=True)
    user_agent = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
