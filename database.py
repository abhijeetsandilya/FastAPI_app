from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("URL_DATABASE")

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

class Base(DeclarativeBase):
    pass