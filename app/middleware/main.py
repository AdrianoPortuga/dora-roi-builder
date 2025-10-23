# app/main.py â€” MODO SEGURO (sem AuditMiddleware)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ðŸ‘‰ tente importar seus routers reais (ajuste os caminhos se necessÃ¡rio)
#   Estruturas comuns: app.routers, app.api, app.routes
routers = {}
for mod in ("app.routers.auth", "app.api.auth", "app.routes.auth"):
    try:
        auth_mod = __import__(mod, fromlist=["router"])
        routers["auth"] = auth_mod.router
        break
    except Exception:
        pass

for mod in ("app.routers.vendors", "app.api.vendors", "app.routes.vendors"):
    try:
        vendors_mod = __import__(mod, fromlist=["router"])
        routers["vendors"] = vendors_mod.router
        break
    except Exception:
        pass

app = FastAPI(
    title="DORA RoI Builder API",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS pro React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health simples
@app.get("/health", tags=["infra"])
def health():
    return {"status": "ok"}

# Anexa routers se existirem
if "auth" in routers:
    app.include_router(routers["auth"], prefix="/api/auth", tags=["auth"])
if "vendors" in routers:
    app.include_router(routers["vendors"], prefix="/api/vendors", tags=["vendors"])

# ðŸ‘‰ Se os seus routers reais nÃ£o forem encontrados,
#    vocÃª ainda terÃ¡ /health e /docs funcionando.
