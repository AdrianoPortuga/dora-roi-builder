# app/middleware/audit.py
import logging
import time
from typing import Iterable, Tuple, Optional

from app.db import SessionLocal
from app.models.audit_log import AuditLog

logger = logging.getLogger("audit")

# Paths que NÃO devem ser auditados (infra/auto):
SKIP_PATHS = {
    "/health",
    "/favicon.ico",
    "/docs",
    "/redoc",
    "/openapi.json",
}

def _get_header(headers: Optional[Iterable[Tuple[bytes, bytes]]], name: str) -> Optional[str]:
    """Obtém um header por nome (case-insensitive)."""
    if not headers:
        return None
    name = name.lower()
    for k, v in headers:
        if k.decode(errors="ignore").lower() == name:
            return v.decode(errors="ignore")
    return None

class AuditMiddleware:
    """
    Middleware de auditoria:
    - ignora rotas de infra (health/docs/openapi/redoc/favicon)
    - mede latência
    - tenta gravar no banco; falhas NÃO derrubam a request (logam aviso)
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Apenas HTTP (ignora websockets/lifespan)
        if scope.get("type") != "http":
            return await self.app(scope, receive, send)

        path = scope.get("path") or "/"
        if path in SKIP_PATHS:
            return await self.app(scope, receive, send)

        method = scope.get("method")
        query_string = scope.get("query_string", b"").decode() or None

        # IP do cliente
        client = scope.get("client") or ("", 0)
        ip = client[0] if isinstance(client, tuple) and len(client) > 0 else None

        # Headers úteis
        headers = scope.get("headers") or []
        user_agent = _get_header(headers, "user-agent")
        # Se você propaga usuário via header (ex.: X-User-Email), pode capturar:
        user_email = _get_header(headers, "x-user-email")  # opcional
        # user_id poderia vir de um token decodificado no seu AuthMiddleware/dep.

        start = time.perf_counter()

        async def send_wrapper(message):
            if message.get("type") == "http.response.start":
                status_code = int(message.get("status", 0))
                latency_ms = int((time.perf_counter() - start) * 1000)

                # Tenta gravar o audit — falha não interrompe a resposta
                try:
                    with SessionLocal() as db:
                        db.add(AuditLog(
                            user_id=None,                    # preencha se você tiver
                            user_email=user_email,           # opcional (header)
                            method=method,
                            path=path,
                            query=query_string,
                            status_code=status_code,
                            latency_ms=latency_ms,
                            ip=ip,
                            user_agent=user_agent,
                            error=None,
                        ))
                        db.commit()
                except Exception as exc:
                    logger.warning("[AUDIT] falha ao gravar audit: %s", exc)

            # segue o fluxo normal da resposta
            await send(message)

        # delega a execução para o app com nosso wrapper de send
        return await self.app(scope, receive, send_wrapper)
