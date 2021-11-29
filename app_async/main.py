"""Run the API."""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.api_v1.api import api_router
from core.config import settings
from db.database import database


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


@app.on_event("startup")
async def startup():
    """Open the connection with to the database."""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Close the connection with the database."""
    await database.disconnect()


# Call the routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# To redirect to docs directly.
@app.get("/")
async def docs_redirect():
    """Redirect to the docs URL."""
    return RedirectResponse(url='/docs')
