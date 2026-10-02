from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import encrypt_secret
from app.core.auth import Role,require_roles
from app.models.device import Device,DeviceType
from app.schemas.device import DeviceCreate,DeviceRead,DeviceUpdate
from app.api.dependencies import routeros_config
from app.plugins.mikrotik.routeros_api import RouterOSError
from app.services.mikrotik_service import MikroTikService
from app.plugins.olt.snmp_poller import SNMPConfig,SNMPError,SNMPPoller
import json
router=APIRouter(prefix="/api/v1/devices",tags=["devices"])
def validate_live(b:DeviceCreate)->None:
 if not b.password: raise HTTPException(422,"Device credentials are required for live validation")
 if b.type==DeviceType.MIKROTIK:
  try:MikroTikService(__import__("app.plugins.mikrotik.routeros_api",fromlist=["RouterOSConfig"]).RouterOSConfig(b.host,b.username or "",b.password,port=b.port or (8729 if b.tls else 8728),tls=b.tls)).test_connection()
  except RouterOSError as e:raise HTTPException(502,f"MikroTik validation failed: {e}") from e
 elif b.type==DeviceType.OLT:
  try:
   import asyncio
   asyncio.run(SNMPPoller(SNMPConfig(b.host,b.password,port=b.port or 161)).test_connection())
  except (SNMPError,OSError) as e:raise HTTPException(502,f"OLT SNMP validation failed: {e}") from e
@router.post("",response_model=DeviceRead,status_code=201,dependencies=[Depends(require_roles(Role.ADMIN,Role.TECHNICIAN))])
def create(b:DeviceCreate,db:Session=Depends(get_db)):
 if db.query(Device).filter(Device.name==b.name).first():raise HTTPException(409,"Device name already exists")
 validate_live(b)
 d=b.model_dump(exclude={"password"})
 d["encrypted_password"]=encrypt_secret(b.password)
 o=Device(**d);db.add(o);db.commit();db.refresh(o);return o
@router.get("",response_model=list[DeviceRead],dependencies=[Depends(require_roles(Role.ADMIN,Role.TECHNICIAN))])
def list_all(db:Session=Depends(get_db)):return db.query(Device).order_by(Device.id).all()
@router.get("/{id}",response_model=DeviceRead,dependencies=[Depends(require_roles(Role.ADMIN,Role.TECHNICIAN))])
def get(id:int,db:Session=Depends(get_db)):
 o=db.get(Device,id)
 if not o:raise HTTPException(404,"Device not found")
 return o
@router.patch("/{id}",response_model=DeviceRead,dependencies=[Depends(require_roles(Role.ADMIN,Role.TECHNICIAN))])
def update(id:int,b:DeviceUpdate,db:Session=Depends(get_db)):
 o=db.get(Device,id)
 if not o:raise HTTPException(404,"Device not found")
 d=b.model_dump(exclude_unset=True);p=d.pop("password",None)
 if p is not None:o.encrypted_password=encrypt_secret(p)
 for k,v in d.items():setattr(o,k,v)
 db.commit();db.refresh(o);return o
@router.delete("/{id}",status_code=204,dependencies=[Depends(require_roles(Role.ADMIN))])
def delete(id:int,db:Session=Depends(get_db)):
 o=db.get(Device,id)
 if not o:raise HTTPException(404,"Device not found")
 db.delete(o);db.commit()
