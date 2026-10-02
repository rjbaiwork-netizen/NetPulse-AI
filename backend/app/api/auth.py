from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel,Field
from app.core.auth import Role,Token,TokenData,create_access_token,hash_password,verify_password,current_user
router=APIRouter(prefix="/api/v1/auth",tags=["auth"])
# Bootstrap/admin credentials are supplied through environment; no default password is accepted.
ADMIN_USER="NETPULSE_ADMIN_USERNAME"; ADMIN_HASH="NETPULSE_ADMIN_PASSWORD_HASH"
class LoginRequest(BaseModel): username:str=Field(min_length=3,max_length=128); password:str=Field(min_length=8,max_length=256)
@router.post("/login",response_model=Token)
def login(body:LoginRequest):
 import os
 username=os.getenv(ADMIN_USER,"")
 password_hash=os.getenv(ADMIN_HASH,"")
 if not username or not password_hash: raise HTTPException(503,"Authentication is not configured")
 if body.username!=username or not verify_password(body.password,password_hash): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials",headers={"WWW-Authenticate":"Bearer"})
 return Token(access_token=create_access_token(username,Role.ADMIN),role=Role.ADMIN)
@router.get("/me",response_model=TokenData)
async def me(user:TokenData=Depends(current_user)): return user
