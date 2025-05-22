# app/db/database.py
import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import get_core_settings

settings = get_core_settings()

def get_database_url():
    """Construct database URL based on environment"""
    postgres_host = settings.POSTGRES_HOST
    postgres_user = settings.POSTGRES_USER
    postgres_password = settings.POSTGRES_PASSWORD
    postgres_db = settings.POSTGRES_DB
    
    # Check if we're running in Cloud Run with Cloud SQL
    if postgres_host.startswith('/cloudsql/'):
        # Cloud SQL Unix socket connection
        return f"postgresql://{postgres_user}:{postgres_password}@/{postgres_db}?host={postgres_host}"
    else:
        # TCP connection (local development or external)
        postgres_port = os.getenv('POSTGRES_PORT', '5432')
        return f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

database_url = get_database_url()
print(f"🔌 Connecting to database: {database_url.replace(settings.POSTGRES_PASSWORD, '*****')}")

engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=300)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


Base.metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()