# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, vendors

app = FastAPI(title="DORA RoI Builder API", version="0.1.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/health", tags=["infra"])
def health(): return {"status": "ok"}

app.include_router(auth.router,    prefix="/api/auth",    tags=["auth"])
app.include_router(vendors.router, prefix="/api/vendors", tags=["vendors"])
