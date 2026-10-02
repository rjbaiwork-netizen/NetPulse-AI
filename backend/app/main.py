from fastapi import FastAPI

app = FastAPI(
    title="NetPulse-AI",
    version="0.1.0",
    description="Pure NMS & AI NOC backend.",
)

@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "netpulse-ai"}
