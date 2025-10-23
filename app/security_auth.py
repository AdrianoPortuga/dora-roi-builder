from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from .models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/token")
ALGORITHM = "HS256"

def create_token(sub: str, expires_delta: timedelta) -> str:
    payload = {"sub": sub, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

def verify_password(plain: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(plain, hashed)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive or not found")
    return user
