from fastapi import FastAPI

from .config import settings
from .models.base import Base
from .models.organization import Organization  # noqa
from .models.user import User  # noqa
from .models.role import Role, RolePermission, UserRole  # noqa
from .models.vendor import Vendor  # noqa

from .database import engine
from .routers.auth import router as auth_router
from .routers.vendors import router as vendors_router

# >>> middleware de auditoria
from .middleware.audit import AuditMiddleware

def create_app():
    app = FastAPI(title="DORA RoI Builder API", version="0.1.0")
    @app.get("/health")
    def health():
        return {"status": "ok"}
    return app

# Exemplo simples (pode manter se ainda não tem nada):
app = FastAPI(title="DORA RoI Builder API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

app = FastAPI(
    title=settings.project_name,
    swagger_ui_parameters={"persistAuthorization": True},
)

# Em SQLite cria tabelas automaticamente; em Postgres usamos Alembic
if settings.database_url.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

# >>> REGISTRA o middleware (linha essencial!)
app.add_middleware(AuditMiddleware)

# opcional: mostrar a pilha de middlewares no boot
print("[BOOT] user_middleware =", app.user_middleware)

# Routers
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(vendors_router, prefix=settings.api_v1_prefix)

@app.get("/")
def root():
    return {"ok": True, "service": settings.project_name}
