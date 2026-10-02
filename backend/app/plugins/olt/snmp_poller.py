from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
from pysnmp.hlapi.v3arch.asyncio import SnmpEngine,CommunityData,UdpTransportTarget,ContextData,ObjectType,ObjectIdentity,get_cmd
class SNMPError(Exception): pass
@dataclass(frozen=True)
class SNMPConfig: host:str; community:str; port:int=161; timeout:float=2.0; retries:int=1; version:int=2
@dataclass(frozen=True)
class ONUTelemetry: signal_dbm:float|None=None; attenuation_db:float|None=None; oper_status:str|None=None; los:bool|None=None; dying_gasp:bool|None=None; timestamp:datetime|None=None
class SNMPPoller:
 def __init__(self,config:SNMPConfig): self.config=config
 async def get(self,*oids:str)->dict[str,str]:
  if not oids:return {}
  engine=SnmpEngine()
  try:
   target=await UdpTransportTarget.create((self.config.host,self.config.port),timeout=self.config.timeout,retries=self.config.retries)
   auth=CommunityData(self.config.community,mpModel=1 if self.config.version==2 else 0)
   ei,es,idx,vbs=await get_cmd(engine,auth,target,ContextData(),*[ObjectType(ObjectIdentity(o)) for o in oids])
   if ei:raise SNMPError(str(ei))
   if es:raise SNMPError(f"SNMP {es.prettyPrint()} at index {idx}")
   return {str(n):v.prettyPrint() for n,v in vbs}
  finally:
   close=getattr(engine,"closeDispatcher",None)
   if close:close()
 async def test_connection(self)->dict[str,str]:
  raw=await self.get("1.3.6.1.2.1.1.1.0")
  return {"status":"connected","sys_descr":next(iter(raw.values()),"unknown")}
 async def poll_onu(self,signal_oid=None,attenuation_oid=None,oper_status_oid=None,los_oid=None,dying_gasp_oid=None):
  oids=[o for o in (signal_oid,attenuation_oid,oper_status_oid,los_oid,dying_gasp_oid) if o]; raw=await self.get(*oids)
  def s(o):return raw.get(o) if o else None
  def n(o):
   try:return float(s(o)) if s(o) is not None else None
   except (TypeError,ValueError):return None
  def b(o):return str(s(o)).lower() in {"1","true","yes","on","up","alarm","los"}
  return ONUTelemetry(n(signal_oid),n(attenuation_oid),s(oper_status_oid),b(los_oid) if los_oid else None,b(dying_gasp_oid) if dying_gasp_oid else None,datetime.now(timezone.utc))
def classify_fault(t:ONUTelemetry)->str:
 if t.dying_gasp is True:return "DYING_GASP"
 if t.los is True or (t.oper_status and t.oper_status.lower() in {"down","2"}):return "FIBER_CUT_OR_LOS"
 return "HEALTHY"
