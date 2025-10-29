# app/main.py

from fastapi import FastAPI
from .api import api_router
from fastapi.middleware.cors import CORSMiddleware


### TODO: Remove hardcoded values and use settings from config.py
app = FastAPI(
    title="WPL API v1",
    description="Wayback Public Library API",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173/",
    # Add any other origins you might use for development.
    # The "*" wildcard is permissive for local development.
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all standard HTTP methods
    allow_headers=["*"],  # Allows all headers
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