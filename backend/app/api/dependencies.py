from fastapi import HTTPException
from app.models.device import Device,DeviceType
from app.core.security import decrypt_secret
from app.plugins.mikrotik.routeros_api import RouterOSConfig
def routeros_config(d:Device)->RouterOSConfig:
 if d.type!=DeviceType.MIKROTIK:raise HTTPException(400,"Device is not MikroTik")
 if not d.username or not d.encrypted_password:raise HTTPException(400,"Device credentials are not configured")
 try:p=decrypt_secret(d.encrypted_password)
 except Exception as e:raise HTTPException(500,"Stored credential cannot be decrypted") from e
 return RouterOSConfig(d.host,d.username,p,port=d.port or 8729,tls=d.tls)
