
# main.py — DORA RoI Builder

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ==== Config / DB ====
from app.config import settings
from app.database import engine
from app.models.base import Base

# importe TODOS os modelos que precisam existir nas tabelas
from app.models.organization import Organization  # noqa
from app.models.user import User  # noqa
from app.models.role import Role, RolePermission, UserRole  # noqa
from app.models.vendor import Vendor  # noqa
from app.models.audit import AuditLog  # noqa  <-- necessário para criar a tabela auditlog

# routers e middleware
from app.routers.auth import router as auth_router
from app.routers.vendors import router as vendors_router
from app.middleware.audit import AuditMiddleware


# --- DEBUG de persistência ---
import os, pathlib
print(f"[DB-DEBUG] DATABASE_URL em uso: {settings.database_url}")
if settings.database_url.startswith("sqlite"):
    path = settings.database_url.split("sqlite:///")[-1].lstrip("/")
    print(f"[DB-DEBUG] Arquivo SQLite (aprox.): {path}")
    print(f"[DB-DEBUG] Existe? {os.path.exists(path)}  |  Absoluto? {pathlib.Path(path).is_absolute()}")
# --- fim do DEBUG ---

# ==== FastAPI app (uma única instância) ====
app = FastAPI(
    title=getattr(settings, "project_name", "DORA RoI Builder API"),
    version=getattr(settings, "version", "0.2"),
    swagger_ui_parameters={"persistAuthorization": True},
)

# ==== CORS (atenção: parênteses fechados) ====
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck
@app.get("/health")
def health():
    return {"status": "ok"}

# Em SQLite cria tabelas automaticamente; em Postgres usar Alembic
if settings.database_url.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

# Middleware de auditoria (depois do create_all tudo já existe)
app.add_middleware(AuditMiddleware)

# Prefixo (garante alinhamento com o front)
api_prefix = getattr(settings, "api_v1_prefix", "/api/v1")
app.include_router(auth_router, prefix=api_prefix)
app.include_router(vendors_router, prefix=api_prefix)

@app.get("/")
def root():
    return {"ok": True, "service": getattr(settings, "project_name", "DORA RoI Builder")}

#| Set-Content -Path C:\dora-roi-builder\main.py -Encoding UTF8
# === CORS habilitado para o front em 5173 ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# === CORS habilitado para o front em 5173 ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
