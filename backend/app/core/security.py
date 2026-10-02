from __future__ import annotations
import base64,hashlib,os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
class SecretManager:
 def __init__(self,key:bytes|None=None):
  raw=key or os.getenv("NETPULSE_ENCRYPTION_KEY","").encode()
  if not raw: raise RuntimeError("NETPULSE_ENCRYPTION_KEY is required")
  try: raw=base64.urlsafe_b64decode(raw)
  except Exception: pass
  self._key=raw if len(raw)==32 else hashlib.sha256(raw).digest()
 def encrypt(self,value:str)->str:
  n=os.urandom(12); return base64.urlsafe_b64encode(n+AESGCM(self._key).encrypt(n,value.encode(),None)).decode()
 def decrypt(self,value:str)->str:
  raw=base64.urlsafe_b64decode(value); return AESGCM(self._key).decrypt(raw[:12],raw[12:],None).decode()
def encrypt_secret(v:str)->str:return SecretManager().encrypt(v)
def decrypt_secret(v:str)->str:return SecretManager().decrypt(v)
