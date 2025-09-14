from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL Database URL (commented out)
# DATABASE_URL = "postgresql://postgres:Munya10*@localhost/omni_db"

# SQLite Database URL
DATABASE_URL = "sqlite:///./omni.db"

# SQLAlchemy Engine
# For SQLite, we need to add connect_args to allow multi-threaded access.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


# Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class for Models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
