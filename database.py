from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# =========================
# DATABASE LOCATION
# =========================

DATABASE_URL = "sqlite:///./smartgrid.db"

# =========================
# CREATE ENGINE
# =========================

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# =========================
# SESSION
# =========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =========================
# BASE CLASS
# =========================

Base = declarative_base()
