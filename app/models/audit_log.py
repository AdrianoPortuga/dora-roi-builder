# app/models/audit_log.py
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from app.db import Base

class AuditLog(Base):
    __tablename__ = "auditlog"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_utc = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    user_id = Column(Integer, nullable=True)
    user_email = Column(Text, nullable=True)

    method = Column(String(10), nullable=False)
    path = Column(Text, nullable=False)
    query = Column(Text, nullable=True)

    status_code = Column(Integer, nullable=False)
    latency_ms = Column(Integer, nullable=False)

    ip = Column(Text, nullable=True)
    user_agent = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
