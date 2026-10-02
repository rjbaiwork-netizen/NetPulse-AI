from pydantic import BaseModel,ConfigDict,Field
class ProfileCreate(BaseModel): name:str; download_bps:int=Field(gt=0); upload_bps:int=Field(gt=0); routeros_profile:str="default"; description:str|None=None
class ProfileRead(ProfileCreate): model_config=ConfigDict(from_attributes=True); id:int
