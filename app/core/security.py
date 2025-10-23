from app.config import settings
# app/core/security.py
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# === Config ===
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-change-me")             # troque em PROD
REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET", "dev-refresh-secret")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MIN = int(os.getenv("ACCESS_EXPIRE_MIN", "60"))
REFRESH_EXPIRE_MIN = int(os.getenv("REFRESH_EXPIRE_MIN", "10080"))       # 7 dias

# Swagger/Authorize usará este endpoint:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/token")

def _create_token(data: Dict[str, Any], minutes: int, secret: str) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

def create_access_token(sub: str) -> str:
    return _create_token({"sub": sub}, ACCESS_EXPIRE_MIN, SECRET_KEY)

def create_refresh_token(sub: str) -> str:
    return _create_token({"sub": sub}, REFRESH_EXPIRE_MIN, REFRESH_SECRET_KEY)

def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

def decode_refresh_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido ou expirado")

def get_current_user(payload: Dict[str, Any] = Depends(lambda token=Depends(oauth2_scheme): decode_access_token(token))):
    # Retorna um dicionário simples do usuário (ajuste para seu modelo real)
    return {"email": payload.get("sub")}


