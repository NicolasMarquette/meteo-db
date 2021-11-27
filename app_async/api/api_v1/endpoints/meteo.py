"""Route for the weather data."""

from typing import List, Optional

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm.session import Session

from api import deps
from db.database import get_db
from schemas import schemas
from crud import crud


router = APIRouter()


@router.get("/meteo", response_model=List[schemas.MeteoBase])
async def get_meteo_from_id(
    station_id: int,
    limit: Optional[int] = 5,
    db_session: Session = Depends(get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    """Give the weather data from the specified station."""
    db_session_meteo = crud.get_meteo_from_id(db_session, station_id=station_id, limit=limit)
    if not db_session_meteo:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return db_session_meteo


@router.get("/meteo/id", response_model=List[schemas.MeteoXYZ])
async def get_meteo_avg_from_id(
    station_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db_session: Session = Depends(get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    """Give the weather data from the specified station."""
    db_session_meteo = crud.get_meteo_avg_from_id(
        db_session,
        station_id=station_id,
        start_date=start_date,
        end_date=end_date
    )
    if not db_session_meteo:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return db_session_meteo


@router.get("/meteo/xyz", response_model=List[schemas.MeteoXYZ])
async def get_meteo_avg_from_xyz(
    x: float,
    y: float,
    z: float,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db_session: Session = Depends(get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
):
    """Give the weather data from the specified station."""
    db_session_meteo = crud.get_meteo_avg_from_xyz(
        db_session,
        x=x,
        y=y,
        z=z,
        start_date=start_date,
        end_date=end_date
    )
    if not db_session_meteo:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return db_session_meteo
