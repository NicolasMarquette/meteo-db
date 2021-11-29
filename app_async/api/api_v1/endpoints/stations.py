"""Route for the station location."""

from typing import List

from fastapi import Depends, HTTPException, Query, APIRouter

from api import deps
from db.database import database
from schemas import schemas
from crud import crud


router = APIRouter()


@router.get("/stations", response_model=List[schemas.StationsBase])
async def get_stations(
    station_id: List[int] = Query(None),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    """Get the location for the specified stations."""
    db_session_station = await crud.get_stations(database, station_id=station_id)
    if not db_session_station:
        raise HTTPException(status_code=404, detail="Stations not found")
    return db_session_station
