import psycopg2
from datetime import datetime
from pathlib import Path
from os import environ
from time import sleep

data_files = environ['WEATHER_DATA_FILES'].split(',')
mounted_path = Path(environ['MOUNTED_DATA_PATH'])

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
    );
"""
with conn.cursor() as curs:
    curs.execute(sql_command)

#Transforming the csv files and copying it to meteo table
for file_name in data_files:
    print(datetime.now(), ' : Processing the file ', file_name)
    
    original_file_name = mounted_path/file_name
    transformed_file_name = (mounted_path/file_name).with_suffix('').with_suffix('._.csv')
    
    with open(original_file_name, 'r') as origin_file:
        with open(transformed_file_name, 'w') as volume_file:
            content = [line for line in origin_file.readlines() if line!='\n']
            volume_file.writelines(content[1:])

    print(f"{datetime.now()} : Inserting file {file_name} into meteo table")
    sql_command = f"""
        COPY meteo (
            station_id,
            lat,
            lon,
            heigth_sta,
            tmp,
            wind_direction,
            wind_speed,
            precip,
            humidity,
            dew_point,
            temperature,
            pressure
        )
        FROM '{transformed_file_name}' 
        DELIMITER ',' 
        CSV;
    """
    with conn.cursor() as curs:
        curs.execute(sql_command)
    
    transformed_file_name.unlink()

#Extracting station data to a separate table
sql_command = """    
    INSERT INTO stations
    SELECT
        station_id, 
        CAST(station_id as VARCHAR(255)),
        ST_GeomFromText(CONCAT('POINT Z(', avg(lat), ' ', avg(lon), ' ', avg(heigth_sta), ')'))
    FROM meteo 
    GROUP BY station_id;
"""
with conn.cursor() as curs:
    curs.execute(sql_command)
    
#Dropping redundant columns and defining foreign key constraint
sql_command = """
    ALTER TABLE meteo
        DROP COLUMN lat,
        DROP COLUMN lon,
        DROP COLUMN heigth_sta,
        ADD FOREIGN KEY (station_id) REFERENCES stations(id);
"""
with conn.cursor() as curs:
    curs.execute(sql_command)
    

print(f"{datetime.now()} : Database is ready !")

conn.close()
