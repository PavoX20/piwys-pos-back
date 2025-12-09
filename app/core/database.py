from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool # <--- 1. IMPORTACIÓN CRÍTICA

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 2. MODIFICAMOS create_engine
engine = create_engine(
    DATABASE_URL,
    # DESACTIVAMOS EL POOL DE SQLALCHEMY para que el pooler de Supabase (6543) trabaje solo
    poolclass=NullPool, 
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para usar en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()