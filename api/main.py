# app/main.py

from fastapi import FastAPI
from .api import api_router

### TODO: Remove hardcoded values and use settings from config.py
app = FastAPI(
    title="WPL API v1",
    description="Wayback Public Library API",
    version="1.0.0",
)

# Main router at ./api.py
app.include_router(api_router)

# Health check endpoint
@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint (health check).
    """
    return {"status": "OK", "message": f"Welcome to WPL API v1"}