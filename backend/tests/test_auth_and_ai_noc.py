import pytest
from app.core import auth
from app.core.auth import Role
from app.api.ai_noc import parse

def test_password_hash_and_verify():
 hashed=auth.hash_password("StrongPass123!")
 assert hashed != "StrongPass123!"
 assert auth.verify_password("StrongPass123!",hashed)
 assert not auth.verify_password("wrong",hashed)

def test_jwt_roundtrip(monkeypatch):
 monkeypatch.setattr(auth,"SECRET","unit-test-secret")
 token=auth.create_access_token("admin",Role.ADMIN)
 import asyncio
 data=asyncio.run(auth.current_user(token))
 assert data.sub=="admin"; assert data.role is Role.ADMIN

@pytest.mark.parametrize(("command","name"),[("show devices","show_devices"),("check signal 7","check_signal"),("kick session 4 alice","kick_session")])
def test_structured_intents(command,name):
 intent=parse(command)
 assert intent.name==name

def test_invalid_intent():
 assert parse("reboot everything").name=="unknown"