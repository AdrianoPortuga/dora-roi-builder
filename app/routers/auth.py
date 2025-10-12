# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_current_user,
)

router = APIRouter()

# ==== MODELOS ====
class LoginBody(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None

# ==== AUTENTICAÇÃO (troque para sua validação real / DB) ====
def authenticate_user(email: str, password: str) -> bool:
    return email == "admin@demo.com" and password == "demo123"

# ---- Login JSON (como você já usava) ----
@router.post("/login", response_model=TokenOut, summary="Login (JSON) → access_token/refresh_token")
def login_json(body: LoginBody):
    if not authenticate_user(body.email, body.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {
        "access_token": create_access_token(body.email),
        "refresh_token": create_refresh_token(body.email),
        "token_type": "bearer",
    }

# ---- Login form (para o botão Authorize do Swagger) ----
@router.post("/token", response_model=TokenOut, summary="OAuth2 Password (form-url-encoded)")
def login_form(form: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form.username, form.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {
        "access_token": create_access_token(form.username),
        "refresh_token": create_refresh_token(form.username),
        "token_type": "bearer",
    }

# ---- Refresh token ----
class RefreshIn(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=TokenOut, summary="Gera novo access_token a partir do refresh_token")
def refresh(body: RefreshIn):
    payload = decode_refresh_token(body.refresh_token)
    sub = payload.get("sub")
    return {
        "access_token": create_access_token(sub),
        "refresh_token": create_refresh_token(sub),
        "token_type": "bearer",
    }

# ---- Usuário atual (usa Authorization: Bearer <access_token>) ----
@router.get("/me", summary="Usuário atual")
def me(user = Depends(get_current_user)):
    if not user or not user.get("email"):
        raise HTTPException(status_code=401, detail="Não autenticado")
    return {"email": user["email"]}
