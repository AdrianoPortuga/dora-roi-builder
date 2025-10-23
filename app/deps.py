import os
from typing import Optional
from types import SimpleNamespace
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    DEV mode:
      - Se DEV_AUTH_ALLOW_ANY=1 -> retorna o primeiro usuário ativo (ex.: admin)
      - Se token começa com 'dev-' -> retorna admin
    PROD mode (sem JWT ainda):
      - 401 (até implementarmos validação JWT real)
    """
    # Bypass total em DEV
    if os.getenv("DEV_AUTH_ALLOW_ANY") == "1":
        user = db.query(User).filter(User.is_active == True).order_by(User.id.asc()).first()
        if not user:
            # Sem usuários no banco: devolve stub em DEV
            return SimpleNamespace(id=0, email="dev@local", is_active=True)
        return user

    # Se recebeu um Bearer dev-..., aceita admin
    if creds and isinstance(creds.credentials, str):
        tok = creds.credentials
        if tok.startswith("dev-"):
            user = db.query(User).filter(User.email == "admin@demo.com").first()
            if user:
                return user

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
