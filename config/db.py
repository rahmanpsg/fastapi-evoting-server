from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@127.0.0.1:3306/db_evoting"

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
