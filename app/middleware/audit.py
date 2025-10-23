from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from app.database import SessionLocal  # <- unificado

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        try:
            resp: Response = await call_next(request)
            status = resp.status_code
            err = None
        except Exception as e:
            status = 500
            err = str(e)
            raise
        finally:
            # grava no auditlog de forma tolerante
            try:
                from app.models.audit import AuditLog  # existe na sua base
                db = SessionLocal()
                db.add(AuditLog(
                    user_id=None,
                    user_email=None,
                    method=request.method,
                    path=request.url.path,
                    query=str(request.url.query) or None,
                    status_code=status,
                    latency_ms=int((time.time()-start)*1000),
                    ip=request.client.host if request.client else None,
                    user_agent=request.headers.get("user-agent"),
                    error=err
                ))
                db.commit()
                db.close()
            except Exception:
                print("[AUDIT] falhou, mas ignorado (dev)")
        return resp
