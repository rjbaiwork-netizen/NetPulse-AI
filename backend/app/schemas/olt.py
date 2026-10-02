from pydantic import BaseModel,Field
class OLTInterfaceRequest(BaseModel): device_id:int; interface_index:int=Field(gt=0)
class ONUPollRequest(BaseModel): device_id:int; signal_oid:str|None=None; attenuation_oid:str|None=None; oper_status_oid:str|None=None; los_oid:str|None=None; dying_gasp_oid:str|None=None
