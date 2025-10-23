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
# app/routers/auth.py
from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

# modelo de entrada (ajuste campos conforme seu schema)
class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginIn, response: Response):
    """
    Endpoint de login (modo desenvolvimento).
    Cria cookie de sessÃ£o compatÃ­vel com HTTP (sem Secure).
    """
    # TODO: troque essa validaÃ§Ã£o pelo teu mÃ©todo real
    if data.email != "admin@codestech.com" or data.password != "admin":
        raise HTTPException(status_code=401, detail="Credenciais invÃ¡lidas")

    # token fake de exemplo â€” substitua pelo JWT real
    token = "fake_dev_token_12345"

    # ðŸ” define cookie compatÃ­vel com dev local
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",   # em dev use 'lax'; para HTTPS cross-site, use 'none'
        secure=False,     # True sÃ³ em produÃ§Ã£o HTTPS
        max_age=60 * 60 * 8,
        path="/",
    )

    return {"ok": True, "message": "Login efetuado com sucesso"}

# ==== MODELOS ====
class LoginBody(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None

# ==== AUTENTICAÃ‡ÃƒO (troque para sua validaÃ§Ã£o real / DB) ====
def authenticate_user(email: str, password: str) -> bool:
    return email == "admin@demo.com" and password == "demo123"

# ---- Login JSON (como vocÃª jÃ¡ usava) ----
@router.post("/login", response_model=TokenOut, summary="Login (JSON) â†’ access_token/refresh_token")
def login_json(body: LoginBody):
    if not authenticate_user(body.email, body.password):
        raise HTTPException(status_code=401, detail="Credenciais invÃ¡lidas")
    return {
        "access_token": create_access_token(body.email),
        "refresh_token": create_refresh_token(body.email),
        "token_type": "bearer",
    }

# ---- Login form (para o botÃ£o Authorize do Swagger) ----
@router.post("/token", response_model=TokenOut, summary="OAuth2 Password (form-url-encoded)")
def login_form(form: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form.username, form.password):
        raise HTTPException(status_code=401, detail="Credenciais invÃ¡lidas")
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

# ---- UsuÃ¡rio atual (usa Authorization: Bearer <access_token>) ----
@router.get("/me", summary="UsuÃ¡rio atual")
def me(user = Depends(get_current_user)):
    if not user or not user.get("email"):
        raise HTTPException(status_code=401, detail="NÃ£o autenticado")
    return {"email": user["email"]}
