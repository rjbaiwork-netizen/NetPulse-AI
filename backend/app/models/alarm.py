from __future__ import annotations
import enum
from datetime import datetime
from sqlalchemy import DateTime,Enum,ForeignKey,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from app.core.database import Base
class AlarmSeverity(str,enum.Enum): INFO="info"; WARNING="warning"; CRITICAL="critical"
class AlarmStatus(str,enum.Enum): OPEN="open"; ACKNOWLEDGED="acknowledged"; RESOLVED="resolved"
class Alarm(Base):
 __tablename__="alarms"; id:Mapped[int]=mapped_column(primary_key=True); device_id:Mapped[int|None]=mapped_column(ForeignKey("devices.id"),nullable=True,index=True); code:Mapped[str]=mapped_column(String(64),index=True); severity:Mapped[AlarmSeverity]=mapped_column(Enum(AlarmSeverity),default=AlarmSeverity.WARNING); status:Mapped[AlarmStatus]=mapped_column(Enum(AlarmStatus),default=AlarmStatus.OPEN,index=True); message:Mapped[str]=mapped_column(Text); evidence_json:Mapped[str|None]=mapped_column(Text,nullable=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); resolved_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
class Incident(Base):
 __tablename__="incidents"; id:Mapped[int]=mapped_column(primary_key=True); title:Mapped[str]=mapped_column(String(200)); status:Mapped[AlarmStatus]=mapped_column(Enum(AlarmStatus),default=AlarmStatus.OPEN); severity:Mapped[AlarmSeverity]=mapped_column(Enum(AlarmSeverity),default=AlarmSeverity.WARNING); summary:Mapped[str]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); resolved_at:Mapped[datetime|None]=mapped_column(DateTime,nullable=True)
