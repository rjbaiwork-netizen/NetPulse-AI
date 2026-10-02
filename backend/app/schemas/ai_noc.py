from pydantic import BaseModel,Field
from typing import Any,Literal
class AICommandRequest(BaseModel):
 command:str=Field(min_length=1,max_length=512)
class AIIntent(BaseModel):
 name:Literal["show_devices","check_signal","kick_session","unknown"]
 parameters:dict[str,Any]
class AICommandResponse(BaseModel):
 intent:AIIntent
 success:bool
 result:Any=None
 message:str
 audit_id:int
