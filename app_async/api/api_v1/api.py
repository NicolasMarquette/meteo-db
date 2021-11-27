"""Create the routes for the API endpoints."""

from fastapi import APIRouter

from api.api_v1.endpoints import login, meteo, stations


# Create the endpoints router.
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(stations.router, tags=["station location"])
api_router.include_router(meteo.router, tags=["weather data"])
