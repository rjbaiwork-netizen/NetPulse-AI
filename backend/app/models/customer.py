from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean,DateTime,ForeignKey,Integer,String
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
class Customer(Base):
 __tablename__="customers"; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(160),index=True); pppoe_username:Mapped[str]=mapped_column(String(128),unique=True,index=True); device_id:Mapped[int|None]=mapped_column(ForeignKey("devices.id"),nullable=True); profile_id:Mapped[int|None]=mapped_column(ForeignKey("pppoe_profiles.id"),nullable=True); active:Mapped[bool]=mapped_column(Boolean,default=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
