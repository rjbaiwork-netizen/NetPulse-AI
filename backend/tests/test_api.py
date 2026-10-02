from fastapi.testclient import TestClient
from app.main import app
from app.core import auth
client=TestClient(app)
def test_health():assert client.get("/health").json()["status"]=="ok"
def test_devices_list(monkeypatch):
 monkeypatch.setattr(auth,"SECRET","ci-test-secret")
 token=auth.create_access_token("ci-admin",auth.Role.ADMIN)
 response=client.get("/api/v1/devices",headers={"Authorization":"Bearer "+token})
 assert response.status_code==200
