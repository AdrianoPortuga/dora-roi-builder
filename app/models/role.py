from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Role(Base):
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)

    __table_args__ = (UniqueConstraint("organization_id", "name", name="uq_role_org_name"),)

class RolePermission(Base):
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False, index=True)
    permission = Column(String(100), nullable=False)

    __table_args__ = (UniqueConstraint("role_id", "permission", name="uq_role_perm"),)

class UserRole(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False, index=True)

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)
