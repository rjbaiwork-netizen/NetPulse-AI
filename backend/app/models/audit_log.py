from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime,Integer,String,Text,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
class AuditLog(Base):
 __tablename__="audit_logs"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 actor:Mapped[str]=mapped_column(String(128),index=True)
 role:Mapped[str]=mapped_column(String(32),index=True)
 action:Mapped[str]=mapped_column(String(128),index=True)
 target:Mapped[str|None]=mapped_column(String(255),nullable=True)
 success:Mapped[bool]=mapped_column(Boolean,default=True)
 detail:Mapped[str|None]=mapped_column(Text,nullable=True)
 created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,index=True)
