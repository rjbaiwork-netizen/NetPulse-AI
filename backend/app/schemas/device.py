from datetime import datetime
from pydantic import BaseModel,Field
from app.models.device import DeviceType
class DeviceBase(BaseModel):
 name:str=Field(min_length=1,max_length=128); type:DeviceType; host:str; port:int=Field(ge=0,le=65535); username:str|None=None; password:str|None=None; tls:bool=True; enabled:bool=True; vendor:str|None=None; latitude:float|None=Field(default=None,ge=-90,le=90); longitude:float|None=Field(default=None,ge=-180,le=180); metadata_json:str|None=None
class DeviceCreate(DeviceBase): pass
class DeviceUpdate(BaseModel):
 name:str|None=None; host:str|None=None; port:int|None=Field(default=None,ge=0,le=65535); username:str|None=None; password:str|None=None; tls:bool|None=None; enabled:bool|None=None; vendor:str|None=None; latitude:float|None=Field(default=None,ge=-90,le=90); longitude:float|None=Field(default=None,ge=-180,le=180); metadata_json:str|None=None
class DeviceRead(BaseModel):
 id:int; name:str; type:DeviceType; host:str; port:int; username:str|None; tls:bool; enabled:bool; vendor:str|None; latitude:float|None; longitude:float|None; metadata_json:str|None; created_at:datetime; updated_at:datetime
 model_config={"from_attributes":True}
