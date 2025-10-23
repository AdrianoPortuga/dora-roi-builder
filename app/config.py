# app/config.py — robusto e tolerante a .env inválido (UTF-8)

from __future__ import annotations

import os
from pathlib import Path
from pydantic_settings import BaseSettings

# dotenv é opcional; se faltar, seguimos só com variáveis de ambiente
try:
    from dotenv import load_dotenv  # type: ignore
except Exception:
    load_dotenv = None  # fallback

# Raiz do repositório (sobe de app/ para a pasta do projeto)
BASE_DIR: Path = Path(__file__).resolve().parents[1]
ENV_PATH: Path = BASE_DIR / ".env"

# Tenta carregar o .env em UTF-8; se o arquivo estiver corrompido/outro encoding, não quebra o app
if load_dotenv and ENV_PATH.exists():
    try:
        load_dotenv(dotenv_path=ENV_PATH, encoding="utf-8")
    except UnicodeDecodeError:
        print("[WARN] .env não está em UTF-8. Ignorando este arquivo. Salve como UTF-8 sem BOM.")

# Caminho ABSOLUTO e estável do SQLite (evita sumiço após reinício)
ROOT_DIR: Path = BASE_DIR
DB_PATH: Path = ROOT_DIR / "dev.db"

class Settings(BaseSettings):
    project_name: str = os.getenv("PROJECT_NAME", "DORA RoI Builder API")
    version: str = os.getenv("VERSION", "0.2")
    api_v1_prefix: str = os.getenv("API_V1_PREFIX", "/api/v1")
    # Default absoluto para o SQLite, caso não exista DATABASE_URL no ambiente
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH.as_posix()}")

    class Config:
        extra = "ignore"  # ignora chaves extras no .env

settings = Settings()
