from __future__ import annotations
import os
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,Session,sessionmaker
DATABASE_URL=os.getenv("DATABASE_URL","sqlite:///./netpulse.db")
engine=create_engine(DATABASE_URL,pool_pre_ping=True,connect_args={"check_same_thread":False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False,expire_on_commit=False)
class Base(DeclarativeBase): pass
def get_db()->Generator[Session,None,None]:
 db=SessionLocal()
 try: yield db
 finally: db.close()
