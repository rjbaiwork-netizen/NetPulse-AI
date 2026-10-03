import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.auth import router as auth_router
from app.api.devices import router as devices_router
from app.api.customers import router as customers_router
from app.api.mikrotik import router as mikrotik_router
from app.api.olt import router as olt_router
from app.api.ai_noc import router as ai_noc_router
from app.models.audit_log import AuditLog
from app.models.customer import Customer, CustomerLocation
app=FastAPI(title="NetPulse-AI",version="0.5.0",description="NMS, customer database, MikroTik/OLT management and AI NOC backend.")
cors_origins=[x.strip() for x in os.getenv("NETPULSE_CORS_ORIGINS","https://rjbaiwork-netizen.github.io,http://localhost:3000").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=cors_origins,allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
Base.metadata.create_all(bind=engine)
app.include_router(auth_router);app.include_router(devices_router);app.include_router(customers_router);app.include_router(mikrotik_router);app.include_router(olt_router);app.include_router(ai_noc_router)
@app.get("/health",tags=["system"])
async def health(): return {"status":"ok","service":"netpulse-ai","version":app.version}
