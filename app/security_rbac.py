from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .security_auth import get_current_user
from .models.role import Role, RolePermission, UserRole
from .models.user import User

def _fetch_user_permissions(user: User, db: Session) -> set[str]:
    # checa se usuÃ¡rio tem papel "admin"
    is_admin = db.query(Role).join(UserRole, UserRole.role_id == Role.id)\
        .filter(UserRole.user_id == user.id, Role.name == "admin").first() is not None
    if is_admin:
        return {"*"}  # wildcard

    rows = (
        db.query(RolePermission.permission)
        .join(Role, RolePermission.role_id == Role.id)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user.id, Role.organization_id == user.organization_id)
        .all()
    )
    return {r[0] for r in rows}

def require_permissions(*required: str):
    """
    Uso: dependencies=[Depends(require_permissions("vendors:read"))]
    """
    def _dep(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        perms = _fetch_user_permissions(user, db)
        if "*" in perms:
            return user
        missing = [p for p in required if p not in perms]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permissions: {missing}",
            )
        return user
    return _dep
