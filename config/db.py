import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('DB_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# meta = MetaData()
# conn = engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# # Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
