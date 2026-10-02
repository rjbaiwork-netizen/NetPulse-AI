from pydantic import BaseModel,ConfigDict,Field
class CustomerCreate(BaseModel): name:str; pppoe_username:str=Field(min_length=1,max_length=128); device_id:int|None=None; profile_id:int|None=None; active:bool=True
class CustomerRead(CustomerCreate): model_config=ConfigDict(from_attributes=True); id:int
