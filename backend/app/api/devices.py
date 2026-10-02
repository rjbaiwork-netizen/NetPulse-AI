from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import encrypt_secret
from app.core.auth import Role,require_roles
from app.models.device import Device
from app.schemas.device import DeviceCreate,DeviceRead,DeviceUpdate
router=APIRouter(prefix="/api/v1/devices",tags=["devices"])
@router.post("",response_model=DeviceRead,status_code=201,dependencies=[Depends(require_roles(Role.ADMIN,Role.TECHNICIAN))])
def create(b:DeviceCreate,db:Session=Depends(get_db)):
 if db.query(Device).filter(Device.name==b.name).first():raise HTTPException(409,"Device name already exists")
 d=b.model_dump(exclude={"password"});d["encrypted_password"]=encrypt_secret(b.password) if b.password else None;o=Device(**d);db.add(o);db.commit();db.refresh(o);return o
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
