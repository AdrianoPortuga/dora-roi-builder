from typing import Optional
import os
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User  # ajuste o import se o modelo estiver noutra pasta

# ===== utils DB =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== models =====
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ===== password verify (aceita pbkdf2_sha256 e bcrypt) =====
from passlib.hash import pbkdf2_sha256
try:
    from passlib.hash import bcrypt as bcrypt_hash
except Exception:
    bcrypt_hash = None

def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    # tenta pbkdf2-sha256
    try:
        if hashed.startswith("$pbkdf2-sha256$"):
            return pbkdf2_sha256.verify(plain, hashed)
    except Exception:
        pass
    # tenta bcrypt
    try:
        if hashed.startswith("$2a$") or hashed.startswith("$2b$") or hashed.startswith("$2y$"):
            if bcrypt_hash:
                return bcrypt_hash.verify(plain, hashed)
    except Exception:
        pass
    # tentativa genérica com pbkdf2
    try:
        return pbkdf2_sha256.verify(plain, hashed)
    except Exception:
        return False

# ===== helpers =====
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def make_dev_token(user: User) -> str:
    # token fake simples para DEV; se já tiver JWT no projeto, integre aqui
    return f"dev-{user.id}-{int(datetime.utcnow().timestamp())}"

router = APIRouter(prefix="/auth", tags=["auth"])

# ===== /auth/login (JSON) =====
@router.post("/login", response_model=TokenResponse)
def login_json(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    # bypass DEV opcional
    if os.getenv("DEV_AUTH_ALLOW_ANY") == "1":
        token = "dev_bypass_token"
        # se sua UI usa cookie, descomente a linha abaixo
        # response.set_cookie("access_token", token, httponly=True, samesite="lax")
        return TokenResponse(access_token=token)

    user = get_user_by_email(db, payload.email)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = make_dev_token(user)
    return TokenResponse(access_token=token)

# ===== /auth/token (OAuth2 Password) =====
@router.post("/token", response_model=TokenResponse)
def oauth2_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2 usa 'username' - aqui tratamos como email
    email = form.username

    if os.getenv("DEV_AUTH_ALLOW_ANY") == "1":
        return TokenResponse(access_token="dev_bypass_token")

    user = get_user_by_email(db, email)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    return TokenResponse(access_token=make_dev_token(user))

# ===== /auth/me (mínimo) =====
@router.get("/me")
def me(db: Session = Depends(get_db)):
    # DEV: se habilitado, devolve um usuário stub caso não exista no banco
    if os.getenv("DEV_AUTH_ALLOW_ANY") == "1":
        user = db.query(User).filter(User.email == "admin@demo.com").first()
        if not user:
            return {
                "id": 0,
                "email": "dev@local",
                "full_name": "Dev User",
                "is_active": True,
            }
        return {
            "id": user.id,
            "email": user.email,
            "full_name": getattr(user, "full_name", None),
            "is_active": bool(user.is_active),
        }

    # PROD: integre com o middleware/JWT e retorne o usuário real.
    user = db.query(User).filter(User.email == "admin@demo.com").first()
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado")
    return {
        "id": user.id,
        "email": user.email,
        "full_name": getattr(user, "full_name", None),
        "is_active": bool(user.is_active),
    }
