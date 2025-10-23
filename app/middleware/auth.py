from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import timedelta
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..config import settings
from ..security_auth import create_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_token(user.email, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh = create_token(user.email, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
