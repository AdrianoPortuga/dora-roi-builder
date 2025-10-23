from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI(title="DORA RoI Builder API")

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class LoginIn(BaseModel):
    email: str
    password: str

@app.post("/api/auth/login")
def login(body: LoginIn):
    # DEMO: aceita qualquer senha para admin@demo.com
    if body.email.lower() != "admin@demo.com":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {
        "access_token": "DEMO_TOKEN",
        "token_type": "bearer",
        "user": {"email": body.email, "name": "Admin Demo"}
    }

@app.get("/api/vendors")
def vendors(token: str = Depends(oauth2)):
    # Se token ausente/errado, OAuth2PasswordBearer já retorna 401
    return [
        {"id": 1, "name": "NovaCo", "country": "BR", "criticality": "low"},
        {"id": 2, "name": "LogTest", "country": "PT", "criticality": "low"},
    ]
