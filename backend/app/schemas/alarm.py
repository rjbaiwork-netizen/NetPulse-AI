from datetime import datetime
from pydantic import BaseModel,ConfigDict
from app.models.alarm import AlarmSeverity,AlarmStatus
class AlarmRead(BaseModel): model_config=ConfigDict(from_attributes=True); id:int; device_id:int|None; code:str; severity:AlarmSeverity; status:AlarmStatus; message:str; evidence_json:str|None; created_at:datetime; resolved_at:datetime|None
class IncidentRead(BaseModel): model_config=ConfigDict(from_attributes=True); id:int; title:str; status:AlarmStatus; severity:AlarmSeverity; summary:str; created_at:datetime; resolved_at:datetime|None
