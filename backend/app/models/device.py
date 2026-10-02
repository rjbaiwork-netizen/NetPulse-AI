from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import Boolean,DateTime,Enum,Integer,String,Text,Float
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
class DeviceType(str,enum.Enum): MIKROTIK="mikrotik"; OLT="olt"; OTHER="other"
class Device(Base):
 __tablename__="devices"
 id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(128),unique=True,index=True); type:Mapped[DeviceType]=mapped_column(Enum(DeviceType),index=True)
 host:Mapped[str]=mapped_column(String(255)); port:Mapped[int]=mapped_column(default=0); username:Mapped[str|None]=mapped_column(String(128),nullable=True); encrypted_password:Mapped[str|None]=mapped_column(Text,nullable=True)
 tls:Mapped[bool]=mapped_column(Boolean,default=True); enabled:Mapped[bool]=mapped_column(Boolean,default=True); vendor:Mapped[str|None]=mapped_column(String(64),nullable=True)
 latitude:Mapped[float|None]=mapped_column(Float,nullable=True); longitude:Mapped[float|None]=mapped_column(Float,nullable=True)
 metadata_json:Mapped[str|None]=mapped_column(Text,nullable=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
