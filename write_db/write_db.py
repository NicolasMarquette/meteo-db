import psycopg2
import pandas as pd
from datetime import datetime

file_path = './data/NW_Ground_Stations_2016.csv'
dbname = "postgres"
user = "postgres"
password = "331295"
host = "localhost"
port = 5432

#Reading the file
print(datetime.now(), ' : Reading the file ', file_path)
df = pd.read_csv(file_path)

#Extracting list of weather stations
df_stations = (df.drop(columns=['date', 'dd', 'ff', 'precip', 'hu', 'td', 't', 'psl'])
                 .drop_duplicates(subset=['number_sta'])
                 .set_index(['number_sta']) 
              )

#Creating station and meteo tables
print(datetime.now(), ' : Creating tables')
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
conn.set_session(readonly=False, autocommit=True)

sql_command = """
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        position GEOGRAPHY(POINTZ) NOT NULL,
        info JSON NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS meteo (
        id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
        station_id INTEGER NOT NULL REFERENCES stations(id),
        tmp TIMESTAMP NOT NULL,
        wind_direction REAL,
        wind_speed REAL,
        precip REAL,
        humidity REAL,
        dew_point REAL,
        temperature REAL,
        pressure REAL
    );
"""

with conn.cursor() as curs:
    curs.execute(sql_command)

#Populating stations table
print(f"{datetime.now()} : Adding {len(df_stations)} weather stations")
for station_id in df_stations.index:
    #Check if the station already exist
    with conn.cursor() as curs:
        curs.execute(f'SELECT COUNT(*) FROM stations WHERE id={station_id}')
        if curs.fetchone()[0] == 0: 
            sql_command = f"""
                INSERT INTO stations (id, name, position, info) VALUES
                ({station_id}, 
                 '{station_id}', 
                 ST_GeomFromText('POINT Z({df_stations.loc[station_id]['lat']} 
                                          {df_stations.loc[station_id]['lon']}
                                          {df_stations.loc[station_id]['height_sta']}
                                         )
                                '),
                 '{{"2016":15}}')
                          """
            curs.execute(sql_command)

#Populating meteo table
print(f"{datetime.now()} : Adding {len(df)} observations")
for row in df.itertuples():
    with conn.cursor() as curs:
        sql_command = f"""
                INSERT INTO meteo (station_id, tmp, wind_direction, wind_speed, precip, humidity,
                                dew_point, temperature, pressure) VALUES
                    ({row.number_sta},
                    '{row.date}',
                    {row.dd if not row.dd else 'NULL'},
                    {row.ff if not row.ff else 'NULL'},
                    {row.precip if not row.precip else 'NULL'},
                    {row.hu if not row.hu else 'NULL'},
                    {row.td if not row.td else 'NULL'},
                    {row.t if not row.t else 'NULL'},
                    {row.psl if not row.psl else 'NULL'}
                    )
                """
        curs.execute(sql_command)

conn.close()
