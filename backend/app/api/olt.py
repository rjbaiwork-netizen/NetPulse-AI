from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import Role,require_roles
from app.core.security import decrypt_secret
from app.models.device import Device,DeviceType
from app.plugins.olt.snmp_poller import SNMPConfig,SNMPError,SNMPPoller,classify_fault
from app.schemas.olt import OLTInterfaceRequest,ONUPollRequest
router=APIRouter(prefix="/api/v1/olt",tags=["olt"])
def poller(id:int,db:Session):
 d=db.get(Device,id)
 if not d or d.type!=DeviceType.OLT:raise HTTPException(404,"OLT device not found")
 if not d.encrypted_password:raise HTTPException(400,"SNMP community is not configured")
 try:c=decrypt_secret(d.encrypted_password)
 except Exception as e:raise HTTPException(500,"Stored SNMP credential cannot be decrypted") from e
 return SNMPPoller(SNMPConfig(d.host,c,port=d.port or 161))
@router.post("/interface/status",dependencies=[Depends(require_roles(Role.ADMIN,Role.TECHNICIAN))])
async def interface_status(b:OLTInterfaceRequest,db:Session=Depends(get_db)):
 try:return await poller(b.device_id,db).get(f"1.3.6.1.2.1.2.2.1.8.{b.interface_index}")
 except SNMPError as e:raise HTTPException(502,str(e))
@router.post("/onu/poll",dependencies=[Depends(require_roles(Role.ADMIN,Role.TECHNICIAN))])
async def onu_poll(b:ONUPollRequest,db:Session=Depends(get_db)):
 try:
  t=await poller(b.device_id,db).poll_onu(b.signal_oid,b.attenuation_oid,b.oper_status_oid,b.los_oid,b.dying_gasp_oid)
  return {"telemetry":t.__dict__,"fault":classify_fault(t)}
 except SNMPError as e:raise HTTPException(502,str(e))
