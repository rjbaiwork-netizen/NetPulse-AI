from __future__ import annotations
import json
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.auth import Role,TokenData,require_roles,current_user
from app.core.database import get_db
from app.models.audit_log import AuditLog
from app.models.device import Device,DeviceType
from app.plugins.olt.snmp_poller import SNMPConfig,SNMPError,SNMPPoller,classify_fault
from app.schemas.ai_noc import AICommandRequest,AICommandResponse,AIIntent
from app.services.mikrotik_service import MikroTikService
from app.api.dependencies import routeros_config
from app.core.security import decrypt_secret
router=APIRouter(prefix="/api/v1/ai-noc",tags=["ai-noc"])
def parse(command:str)->AIIntent:
 p=command.strip().split()
 if len(p)==2 and p[0].lower()=="show" and p[1].lower()=="devices": return AIIntent(name="show_devices",parameters={})
 if len(p)>=2 and p[0].lower()=="check" and p[1].lower()=="signal":
  if len(p)!=3: raise HTTPException(422,"Use: check signal <device-id>")
  try:return AIIntent(name="check_signal",parameters={"device_id":int(p[2])})
  except ValueError: raise HTTPException(422,"Device id must be numeric")
 if len(p)>=3 and p[0].lower()=="kick" and p[1].lower()=="session":
  try: device_id=int(p[2])
  except ValueError: raise HTTPException(422,"Device id must be numeric")
  user=" ".join(p[3:]).strip()
  if not user: raise HTTPException(422,"Use: kick session <device-id> <username>")
  return AIIntent(name="kick_session",parameters={"device_id":device_id,"username":user})
 return AIIntent(name="unknown",parameters={})
def audit(db,actor,role,intent,success,detail,target=None):
 a=AuditLog(actor=actor,role=role.value,action=intent.name,target=target,success=success,detail=detail[:4000] if detail else None);db.add(a);db.commit();db.refresh(a);return a.id
@router.post("/command",response_model=AICommandResponse,dependencies=[Depends(require_roles(Role.ADMIN,Role.TECHNICIAN))])
async def command(body:AICommandRequest,db:Session=Depends(get_db),user:TokenData=Depends(current_user)):
 intent=parse(body.command)
 if intent.name=="unknown":
  aid=audit(db,user.sub,user.role,intent,False,"Unsupported command")
  return AICommandResponse(intent=intent,success=False,message="Supported commands: show devices; check signal <device-id>; kick session <device-id> <username>",audit_id=aid)
 try:
  if intent.name=="show_devices":
   rows=db.query(Device).order_by(Device.id).all()
   result=[{"id":d.id,"name":d.name,"type":d.type.value,"host":d.host,"pop_name":d.pop_name,"latitude":d.latitude,"longitude":d.longitude,"enabled":d.enabled} for d in rows]
  elif intent.name=="kick_session":
   d=db.get(Device,intent.parameters["device_id"])
   if not d: raise HTTPException(404,"Device not found")
   removed=MikroTikService(routeros_config(d)).kick_active_session(intent.parameters["username"])
   result={"device_id":d.id,"username":intent.parameters["username"],"removed_sessions":removed}
  else:
   d=db.get(Device,intent.parameters["device_id"])
   if not d or d.type!=DeviceType.OLT: raise HTTPException(404,"OLT device not found")
   if not d.encrypted_password: raise HTTPException(400,"SNMP community is not configured")
   meta=json.loads(d.metadata_json or "{}")
   required=["signal_oid","attenuation_oid","oper_status_oid","los_oid","dying_gasp_oid"]
   if any(k not in meta for k in required): raise HTTPException(400,"Device metadata must define signal_oid, attenuation_oid, oper_status_oid, los_oid and dying_gasp_oid")
   community=decrypt_secret(d.encrypted_password)
   t=await SNMPPoller(SNMPConfig(d.host,community,port=d.port or 161)).poll_onu(*(meta[k] for k in required))
   result={"device_id":d.id,"telemetry":t.__dict__,"fault":classify_fault(t)}
  aid=audit(db,user.sub,user.role,intent,True,"Command completed",str(intent.parameters))
  return AICommandResponse(intent=intent,success=True,result=result,message="Command completed",audit_id=aid)
 except HTTPException:
  raise
 except (SNMPError,Exception) as e:
  aid=audit(db,user.sub,user.role,intent,False,str(e),str(intent.parameters))
  raise HTTPException(502,"Network operation failed; audit_id="+str(aid)) from e
