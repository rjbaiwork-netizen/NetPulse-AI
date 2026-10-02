from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.device import Device
from app.api.dependencies import routeros_config
from app.plugins.mikrotik.routeros_api import RouterOSError
from app.services.mikrotik_service import MikroTikService,PPPoESecret,MikroTikValidationError
from app.schemas.mikrotik import PPPoESecretCreate,SpeedProfileUpdate,KickRequest
router=APIRouter(prefix="/api/v1/mikrotik",tags=["mikrotik"])
def svc(id:int,db:Session):
 d=db.get(Device,id)
 if not d:raise HTTPException(404,"Device not found")
 return MikroTikService(routeros_config(d))
def fail(e):raise HTTPException(422 if isinstance(e,MikroTikValidationError) else 502,str(e))
@router.post("/{id}/pppoe/secrets")
def add(id:int,b:PPPoESecretCreate,db:Session=Depends(get_db)):
 try:return svc(id,db).add_pppoe_secret(PPPoESecret(b.username,b.password,b.profile,b.service,b.disabled,b.comment))
 except (MikroTikValidationError,RouterOSError) as e:fail(e)
@router.post("/{id}/pppoe/speed")
def speed(id:int,b:SpeedProfileUpdate,db:Session=Depends(get_db)):
 try:return svc(id,db).set_speed_profile(b.username,b.download_bps,b.upload_bps)
 except (MikroTikValidationError,RouterOSError) as e:fail(e)
@router.post("/{id}/pppoe/kick")
def kick(id:int,b:KickRequest,db:Session=Depends(get_db)):
 try:return {"removed_sessions":svc(id,db).kick_active_session(b.username)}
 except (MikroTikValidationError,RouterOSError) as e:fail(e)
