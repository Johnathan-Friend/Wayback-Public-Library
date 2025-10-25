# app/api.py

from fastapi import APIRouter

from .domains.patron import router as patron_router

# API version 1
v1_router = APIRouter(prefix="/api/v1")

# Domain Routers
v1_router.include_router(patron_router)


# Main router for the API
api_router = APIRouter()
api_router.include_router(v1_router)