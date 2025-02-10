from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from configobj import ConfigObj

config = ConfigObj("config.cfg")

ENVIRONMENT = config["SERVICE"].get("MODE", "production")
DATABASE_SECTION = "DATABASE" if ENVIRONMENT == "production" else "TESTS"

MYSQL_USER = config[DATABASE_SECTION]["MYSQL_USER"]
MYSQL_PASSWORD = config[DATABASE_SECTION]["MYSQL_PASSWORD"]
MYSQL_HOST = config[DATABASE_SECTION]["MYSQL_HOST"]
MYSQL_PORT = config[DATABASE_SECTION]["MYSQL_PORT"]
MYSQL_DATABASE = config[DATABASE_SECTION]["MYSQL_DATABASE"]

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
