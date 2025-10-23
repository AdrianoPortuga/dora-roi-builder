﻿# create_tables.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base  # ajuste o caminho do seu Base
# from app.models.audit import AuditLog  # se necessÃ¡rio para registrar o model

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://dora:dora@localhost:5433/dora")
engine = create_engine(DATABASE_URL, future=True)
Base.metadata.create_all(bind=engine)
print("Tabelas criadas")
