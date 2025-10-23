from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import os

# Config e DB
from app.config import settings
from app.database import engine
from app.models.base import Base

# Importa modelos para criação de tabelas (SQLite)
from app.models.organization import Organization  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.role import Role, RolePermission, UserRole  # noqa: F401
from app.models.vendor import Vendor  # noqa: F401
from app.models.audit import AuditLog  # noqa: F401

# Routers
from app.routers import auth, vendors

app = FastAPI(
    title=getattr(settings, "project_name", "DORA RoI Builder API"),
    version=getattr(settings, "version", "0.2"),
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={"persistAuthorization": True},
)

# Redirect raiz -> /docs
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

# CORS para o front local
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health simples
@app.get("/health", tags=["infra"])
def health():
    return {
        "status": "ok",
        "version": getattr(settings, "version", os.getenv("APP_VERSION", "0.1.0")),
        "env": os.getenv("APP_ENV", "local"),
    }

# Cria tabelas automaticamente em SQLite; para Postgres use Alembic
if settings.database_url.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

# Middleware de auditoria (tolerante se ausente)
try:
    from app.middleware.audit import AuditMiddleware  # type: ignore
    app.add_middleware(AuditMiddleware)
except Exception:
    pass

# Prefixo base da API e routers
api_prefix = getattr(settings, "api_v1_prefix", "/api/v1")
app.include_router(auth.router, prefix=api_prefix)
app.include_router(vendors.router, prefix=api_prefix)
