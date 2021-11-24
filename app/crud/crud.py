"""CRUD function."""

from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_station(db_session: Session, station_id: int):
    """Function to get the location of the specified station.

    Parameters
    ----------
    db_session : Session
        The current session for the database.
    station_id : int
        The id of the station which want the location.

    Return
    ------
    dict : A dictionnary with all the data for the station.
    """
    query = text("SELECT *, "
                 "ST_X(position::geometry) AS lat, "
                 "ST_Y(position::geometry) AS long, "
                 "ST_Z(position::geometry) AS height "
                 f"FROM stations WHERE id = {station_id} "
                 "LIMIT 1")
    results = db_session.execute(query).fetchall()
    return  [dict(row) for row in results]


def get_stations(db_session: Session, station_id: List[int]):
    """Function to get the location of the specified stations.

    Parameters
    ----------
    db_session : Session
        The current session for the database.
    station_id : list[int]
        A list of id of the stations which want the location.

    Return
    ------
    dict : A dictionnary with all the data for the stations.
    """
    query = text("SELECT *, "
                 "ST_X(position::geometry) AS lat, "
                 "ST_Y(position::geometry) AS long, "
                 "ST_Z(position::geometry) AS height "
                 f"FROM stations WHERE id IN {tuple(station_id)}")
    results = db_session.execute(query).fetchall()
    return  [dict(row) for row in results]


def get_meteo(db_session: Session, station_id: int):
    """Function to get the weather data for the station specified.

    Parameters
    ----------
    db_session : Session
        The current session for the database.
    station_id : int
        The id of the station which want the location.

    Return
    ------
    dict : A dictionnary with all the weather data for the station.
    """
    query = text(f"select * from meteo WHERE station_id = {station_id} LIMIT 20")
    results = db_session.execute(query).fetchall()
    return  [dict(row) for row in results]
