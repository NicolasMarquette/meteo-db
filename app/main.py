"""Run the API."""

from fastapi import FastAPI

from api.api_v1.api import api_router
from core.config import settings


DESCRIPTION = """
## API to get weather information from several weather stations in France.

### Made by
* Nicolas Marquette & Marcello Caciolo
* 2021
"""

app = FastAPI(
    title="METEO API",
    description=DESCRIPTION,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=[
        {
            "name": "station location",
            "description": "Route to get the location of one or several stations."
        },
        {
            "name" : "weather data",
            "description": "Route to get the weather data from a station."
        },
        {
            "name": "login",
            "description": "function to login"
        },
    ]
)


# Call the routers
app.include_router(api_router, prefix=settings.API_V1_STR)
