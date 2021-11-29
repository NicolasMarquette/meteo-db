"""CRUD function."""

from typing import List

from databases import Database
from sqlalchemy import text


async def get_stations(database: Database, station_id: List[int]):
    """Function to get the location of the specified stations.

    Parameters
    ----------
    database : Session
        The current session for the database.
    station_id : list[int]
        A list of id of the stations which want the location.

    Return
    ------
    dict : A dictionnary with all the data for the stations.
    """
    if not station_id:
        return []
    else:
        if len(station_id) == 1:
            stations_id = f"({station_id[0]})"
        else:
            stations_id = str(tuple(station_id))

        query = text("SELECT *, "
                    "ST_X(position::geometry) AS lat, "
                    "ST_Y(position::geometry) AS long, "
                    "ST_Z(position::geometry) AS height "
                    f"FROM stations WHERE id IN {stations_id};")
        results = await database.fetch_all(query)
        return  [dict(row) for row in results]


async def get_meteo_from_id(database: Database, station_id: int, limit: int):
    """Function to get the weather data for the station specified.

    Parameters
    ----------
    database : Session
        The current session for the database.
    station_id : int
        The id of the station which want the location.
    limit : int : default=5
        The number of data returned by the query.

    Return
    ------
    dict : A dictionnary with the limit number of the weather data for the station.
    """
    query = text("SELECT * "
                 "FROM meteo "
                 f"WHERE station_id = {station_id} "
                 "ORDER BY tmp DESC "
                 f"LIMIT {limit};")
    results = await database.fetch_all(query)
    return  [dict(row) for row in results]



async def get_meteo_avg_from_id(database: Database, station_id: int,
                       start_date: str, end_date: str
):
    """Function to get the weather data for the specified station id.

    Parameters
    ----------
    database : Session
        The current session for the database.
    station_id : int
        The id of the station which want the location.
    start_date : str : default=None
        The starting date for searching data begining in this date.
    end_date : str : default=None
        The ending date for searching data ending in this date.

    Return
    ------
    dict : A dictionnary with all the weather data for the station.
    """
    # Check if date are entered.
    if not start_date:
        date_query = ""
        end_date = start_date
    else:
        if not end_date:
            end_date = start_date
        date_query = f"AND (meteo.tmp BETWEEN '{start_date}' AND '{end_date}')"

    query = text(
    "SELECT  meteo.station_id AS id, "
            "ST_AsText(stations.position) AS position, "
            f"'{start_date}' AS start_date, "
            f"'{end_date}' AS end_date, "
            "AVG(meteo.wind_direction) AS avg_wind_direction, "
            "AVG(meteo.wind_speed) AS avg_wind_speed, "
            "AVG(meteo.precip) AS avg_precip, "
            "AVG(meteo.humidity) AS avg_humidity, "
            "AVG(meteo.dew_point) AS avg_dew_point, "
            "AVG(meteo.temperature) AS avg_temperature, "
            "AVG(meteo.pressure) AS avg_pressure, "
            "COUNT(*) AS count_data "
    "FROM meteo, stations "
    "WHERE meteo.station_id = stations.id "
    f"AND meteo.station_id = {station_id} "
    f"{date_query} "
    "GROUP BY meteo.station_id, position;"
    )

    results = await database.fetch_all(query)
    return  [dict(row) for row in results]


async def get_meteo_avg_from_xyz(database: Database, x: float, y: float, z: float,
                       start_date: str, end_date: str
):
    """Function to get the weather data for the station nearest the point specified.

    Parameters
    ----------
    database : Session
        The current session for the database.
    x : int
        The latitude coordinate.
    y : int
        The longitude coordinate.
    z : int
        The height coordinate.
    start_date : str : default=None
        The starting date for searching data begining in this date.
    end_date : str : default=None
        The ending date for searching data ending in this date.

    Return
    ------
    dict : A dictionnary with all the weather data for the station.
    """
    # Check if date are entered.
    if not start_date:
        date_query = ""
        end_date = start_date
    else:
        if not end_date:
            end_date = start_date
        date_query = f"AND (meteo.tmp BETWEEN '{start_date}' AND '{end_date}')"

    query = text(
    "SELECT  station.id, "
            "station.position, "
            f"'{start_date}' AS start_date, "
            f"'{end_date}' AS end_date, "
            "AVG(meteo.wind_direction) AS avg_wind_direction, "
            "AVG(meteo.wind_speed) AS avg_wind_speed, "
            "AVG(meteo.precip) AS avg_precip, "
            "AVG(meteo.humidity) AS avg_humidity, "
            "AVG(meteo.dew_point) AS avg_dew_point, "
            "AVG(meteo.temperature) AS avg_temperature, "
            "AVG(meteo.pressure) AS avg_pressure, "
            "COUNT(*) AS count_data "
    "FROM meteo, "
    "(SELECT id, ST_AsText(position) AS position, "
        "ST_3DClosestPoint(stations.position::geometry, "
                    f"ST_SetSRID((SELECT 'POINT({x} {y} {z})'::geometry), 4326)) AS point "
        "FROM stations "
        "LIMIT 1"
    ") as station "
    "WHERE meteo.station_id = station.id "
    f"{date_query} "
    "GROUP BY station.id, station.position;"
    )

    results = await database.fetch_all(query)
    return  [dict(row) for row in results]
