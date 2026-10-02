from pydantic import BaseModel,ConfigDict,Field
from app.models.device import DeviceType
class DeviceCreate(BaseModel): name:str=Field(min_length=1,max_length=128); type:DeviceType; host:str; port:int=Field(default=0,ge=0,le=65535); username:str|None=None; password:str|None=None; tls:bool=True; enabled:bool=True; vendor:str|None=None; metadata_json:str|None=None
class DeviceUpdate(BaseModel): name:str|None=None; host:str|None=None; port:int|None=Field(default=None,ge=0,le=65535); username:str|None=None; password:str|None=None; tls:bool|None=None; enabled:bool|None=None; vendor:str|None=None; metadata_json:str|None=None
class DeviceRead(BaseModel): model_config=ConfigDict(from_attributes=True); id:int; name:str; type:DeviceType; host:str; port:int; username:str|None; tls:bool; enabled:bool; vendor:str|None; metadata_json:str|None
