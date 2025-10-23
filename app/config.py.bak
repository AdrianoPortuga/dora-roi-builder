import os
from dataclasses import dataclass
from dotenv import load_dotenv

# carrega o .env a partir da raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(BASE_DIR, ".env"))

@dataclass
class Settings:
    project_name: str = "DORA RoI Builder"
    api_v1_prefix: str = "/api"

    secret_key: str = os.getenv("SECRET_KEY", "changeme-dev")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    cors_origins: list[str] = None

settings = Settings()
