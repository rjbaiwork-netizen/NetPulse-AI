from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():assert client.get("/health").json()["status"]=="ok"
def test_devices_list():assert client.get("/api/v1/devices").status_code==200
