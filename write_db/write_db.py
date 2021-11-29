import psycopg2
from datetime import datetime
from pathlib import Path
from os import environ
from time import sleep
import glob


mounted_path = Path(environ['MOUNTED_DATA_PATH'])
data_files = glob.glob(str(mounted_path/'*.csv'))

dbname = environ['DB_NAME']
user = environ['DB_USER']
password = environ['DB_PASSWORD']
host = environ['DB_HOST']
port = environ['DB_PORT']


print(datetime.now(), ' : Connecting to database')
for i_connection_try in range(3):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    except Exception as ex:
        print(f"{datetime.now()} : Attempt n° {i_connection_try} to connect to the database failed. Waiting 5 seconds...")
        if i_connection_try==2:
            raise ex
        sleep(5)

conn.set_session(readonly=False, autocommit=True)

#Creating tables
print(datetime.now(), ' : Creating tables')

sql_command = """
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        position GEOGRAPHY(POINTZ) NOT NULL
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
    
#Processed file directory
(mounted_path / 'processed').mkdir(exist_ok=True)

#Transforming the csv files and copying it to meteo table
for file_name in data_files:
    print(datetime.now(), ' : Processing the file ', file_name)
    
    original_file_name = mounted_path/file_name
    transformed_file_name = (mounted_path/file_name).with_suffix('').with_suffix('._.csv')
    
    with open(original_file_name, 'r') as origin_file:
        with open(transformed_file_name, 'w') as volume_file:
            volume_file.write("".join([line for line in origin_file.readlines() if line!='\n'][1:]))

    print(f"{datetime.now()} : Inserting file {file_name} into meteo table")
    sql_command = f"""
    
        CREATE EXTENSION IF NOT EXISTS file_fdw;
        
        CREATE SERVER IF NOT EXISTS srv_file_fdw FOREIGN DATA WRAPPER file_fdw;
        
        CREATE FOREIGN TABLE meteo_temp(
            station_id INTEGER NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            heigth_sta REAL NOT NULL,
            tmp TIMESTAMP NOT NULL,
            wind_direction REAL,
            wind_speed REAL,
            precip REAL,
            humidity REAL,
            dew_point REAL,
            temperature REAL,
            pressure REAL
        )
            SERVER srv_file_fdw
            OPTIONS (FILENAME '{transformed_file_name}', FORMAT 'csv');

        INSERT INTO stations
            SELECT st.station_id, st.name, st.position FROM 
            (
                SELECT
                    station_id, 
                    CAST(station_id as VARCHAR(255)) as name,
                    ST_GeomFromText(CONCAT('POINT Z(', avg(lat), ' ', avg(lon), ' ', avg(heigth_sta), ')')) as position
                FROM meteo_temp
                GROUP BY station_id
            ) st
            WHERE station_id NOT IN (SELECT id FROM stations);
            
        INSERT INTO meteo (
            station_id,
            tmp,
            wind_direction,
            wind_speed,
            precip,
            humidity,
            dew_point,
            temperature,
            pressure
        )
            SELECT
                station_id,
                tmp,
                wind_direction,
                wind_speed,
                precip,
                humidity,
                dew_point,
                temperature,
                pressure
            FROM meteo_temp;
            
        DROP FOREIGN TABLE meteo_temp;
        
        DROP SERVER srv_file_fdw;
        
        DROP EXTENSION file_fdw; 
    """
    with conn.cursor() as curs:
        curs.execute(sql_command)
    
    #Move the procedded file and delete the transformed one
    original_file_name.replace(original_file_name.parent / 'processed' / original_file_name.name)
    transformed_file_name.unlink()

print(f"{datetime.now()} : Database is ready !")

conn.close()
