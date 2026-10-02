from fastapi import FastAPI
from app.core.database import Base,engine
from app.api.auth import router as auth_router
from app.api.devices import router as devices_router
from app.api.mikrotik import router as mikrotik_router
from app.api.olt import router as olt_router
app=FastAPI(title="NetPulse-AI",version="0.3.0",description="Pure NMS & AI NOC backend.")
Base.metadata.create_all(bind=engine)
app.include_router(auth_router);app.include_router(devices_router);app.include_router(mikrotik_router);app.include_router(olt_router)
@app.get("/health",tags=["system"])
async def health():return {"status":"ok","service":"netpulse-ai"}
