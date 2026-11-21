"""API v1 package."""
from fastapi import APIRouter
from app.api.v1.endpoints import producers, deliveries, factoring, dashboard

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(producers.router, prefix="/producers", tags=["Producers"])
api_router.include_router(deliveries.router, prefix="/deliveries", tags=["Acopio & Boleta Transparente"])
api_router.include_router(factoring.router, prefix="/factoring", tags=["Oráculo IA & Factoring"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard & Vaquita Pool"])
