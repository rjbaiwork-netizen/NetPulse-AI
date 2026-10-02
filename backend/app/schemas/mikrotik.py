from pydantic import BaseModel,Field
class PPPoESecretCreate(BaseModel): username:str=Field(min_length=1,max_length=128); password:str=Field(min_length=1,max_length=256); profile:str="default"; service:str="pppoe"; disabled:bool=False; comment:str|None=None
class SpeedProfileUpdate(BaseModel): username:str; download_bps:int=Field(gt=0); upload_bps:int=Field(gt=0)
class KickRequest(BaseModel): username:str=Field(min_length=1,max_length=128)
