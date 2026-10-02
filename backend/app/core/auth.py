from __future__ import annotations
import os
from datetime import datetime,timedelta,timezone
from enum import Enum
from typing import Annotated
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from passlib.context import CryptContext
from pydantic import BaseModel
SECRET=os.getenv("NETPULSE_JWT_SECRET","")
ALGORITHM="HS256"; ACCESS_MINUTES=int(os.getenv("NETPULSE_ACCESS_TOKEN_MINUTES","30"))
pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
class Role(str,Enum): ADMIN="admin"; TECHNICIAN="technician"
class Token(BaseModel): access_token:str; token_type:str="bearer"; role:Role
class TokenData(BaseModel): sub:str; role:Role
def hash_password(value:str)->str:return pwd.hash(value)
def verify_password(plain:str,hashed:str)->bool:return pwd.verify(plain,hashed)
def create_access_token(subject:str,role:Role)->str:
 if not SECRET: raise RuntimeError("NETPULSE_JWT_SECRET is required")
 now=datetime.now(timezone.utc); return jwt.encode({"sub":subject,"role":role.value,"iat":now,"exp":now+timedelta(minutes=ACCESS_MINUTES)},SECRET,algorithm=ALGORITHM)
async def current_user(token:Annotated[str,Depends(oauth2)]) -> TokenData:
 if not SECRET: raise HTTPException(503,"Authentication is not configured")
 exc=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired authentication token",headers={"WWW-Authenticate":"Bearer"})
 try:
  data=jwt.decode(token,SECRET,algorithms=[ALGORITHM]); return TokenData(sub=str(data["sub"]),role=Role(data["role"]))
 except (JWTError,KeyError,ValueError): raise exc
def require_roles(*roles:Role):
 async def checker(user:Annotated[TokenData,Depends(current_user)]):
  if user.role not in roles: raise HTTPException(403,"Insufficient role")
  return user
 return checker
