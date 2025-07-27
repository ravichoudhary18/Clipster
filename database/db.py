from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import BASE_DIR
from logger import logger

# Define DB path
DB_PATH = BASE_DIR / "db.sqlite3"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

session = SessionLocal()


def database_create():
    if not DB_PATH.exists():
        logger.info("DATABASE CREATED")
        DB_PATH.touch()
