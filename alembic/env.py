from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models.audit_log import AuditLog  # noqa

# imports necessários
import os
import sys

# permitir importar o pacote 'app' (sobe um nível a partir de alembic/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Settings e Models do app
from app.config import settings
from app.models.base import Base
from app.models.organization import Organization  # noqa
from app.models.user import User  # noqa
from app.models.role import Role, RolePermission, UserRole  # noqa
from app.models.vendor import Vendor  # noqa  # (se existir Vendors)

# pega config do Alembic e injeta a URL do nosso Settings
config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

# logging do alembic.ini (opcional)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata para autogenerate
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"client_encoding": "utf8"},  # ajuda com encoding no Windows
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
