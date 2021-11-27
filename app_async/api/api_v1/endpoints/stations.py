"""Route for the station location."""

from typing import List

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm.session import Session

from api import deps
from db.database import get_db
from schemas import schemas
from crud import crud


router = APIRouter()


@router.get("/stations", response_model=List[schemas.StationsBase])
async def get_stations(
    station_id: List[int] = Query(None),
    db_session: Session = Depends(get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    """Get the location for the specified stations."""
    db_session_station = crud.get_stations(db_session, station_id=station_id)
    if not db_session_station:
        raise HTTPException(status_code=404, detail="Stations not found")
    return db_session_station
