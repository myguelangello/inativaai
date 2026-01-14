import os
from sqlalchemy import create_engine
import oracledb
import psycopg2
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

host = os.environ.get("ORACLE_HOST")
port = os.environ.get('ORACLE_PORT')
service_name = os.environ.get("ORACLE_SID")
user = os.environ.get("ORACLE_USER")
password = os.environ.get("ORACLE_PASS")
password_encoded = quote_plus(password)

RH_HOST = os.getenv("RH_HOST")
RH_USERNAME = os.getenv("RH_USERNAME")
RH_PASSWORD = os.getenv("RH_PASSWORD")
RH_DATABASE = os.getenv("RH_DATABASE")
RH_PORT = os.getenv("RH_PORT")

pass_encoded = quote_plus(RH_PASSWORD)

def connect_oracle_db():
    try:
        engine_oracle = create_engine(
            f"oracle+oracledb://{user}:{password_encoded}@{host}:{port}/?service_name={service_name}",
            pool_recycle=1800,
            pool_pre_ping=True
        )
        connection = engine_oracle.connect()
        return connection
    except oracledb.Error as e:
        return str(e)

def connect_fortesrh_db():
    try:
        engine_postgres = create_engine(
            f"postgresql+psycopg2://{RH_USERNAME}:{pass_encoded}@{RH_HOST}:{RH_PORT}/{RH_DATABASE}",
            pool_recycle=1800,
            pool_pre_ping=True
        )
        connection = engine_postgres.connect()
        return connection
    except Exception as e:
        print(f"Error in connect_fortesrh_db: {e}")
        return str(e), 500
    except psycopg2.Error as e:
        print(f"Error in connect_fortesrh_db (psycopg2): {e}")