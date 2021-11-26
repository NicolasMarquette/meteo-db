"""Schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StationsBase(BaseModel):
    """Base model for the station."""
    id: int
    name: str
    position: str
    lat: Optional[float]
    long: Optional[float]
    height: Optional[float]


class MeteoBase(BaseModel):
    "Base model for the weather data."
    id: int
    station_id: int
    tmp: datetime
    wind_direction: Optional[float] = None
    wind_speed: Optional[float] = None
    precip: Optional[float] = None
    humidity: Optional[float] = None
    dew_point: Optional[float] = None
    temperature: Optional[float] = None
    pressure: Optional[float] = None


class MeteoXYZ(BaseModel):
    "Base model for the weather data."
    id: int
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    avg_wind_direction: Optional[float] = None
    avg_wind_speed: Optional[float] = None
    avg_precip: Optional[float] = None
    avg_humidity: Optional[float] = None
    avg_dew_point: Optional[float] = None
    avg_temperature: Optional[float] = None
    avg_pressure: Optional[float] = None
    count_data: int



class Token(BaseModel):
    """Base model for the token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for the data in the token."""
    username: Optional[str] = None


class User(BaseModel):
    """Base model for the users."""
    username: Optional[str] = None
    admin: Optional[bool] = None


class UserInDB(User):
    """Model for the hashed_password in the users database."""
    hashed_password: str
