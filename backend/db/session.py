from functools import lru_cache
import time
from typing import Generator

from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from config import get_settings

# from google.cloud.sql.connector import Connector

# from google.auth import load_credentials_from_file

# # function to return the database connection
# def getconn() -> pymysql.connections.Connection:
#     # initialize Connector object
#     creds = load_credentials_from_file("application_default_credentials.json")

#     connector = Connector(
#         credentials=creds[0]
# )
#     conn: pymysql.connections.Connection = connector.connect(
#         os.getenv("INSTANCE_CONNECTION_STRING"),
#         "pymysql",
#         user=os.getenv("MYSQL_USER_ROOT"),
#         password=os.getenv("MYSQL_ROOT_PASSWORD"),
#         db=os.getenv("MYSQL_DATABASE"),
#     )
#     return conn


def getconn() -> sqlalchemy.Engine:
    MAX_RETRIES = 5
    RETRY_DELAY = 5  # in seconds

    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            engine = create_engine(get_settings().database_url)
            break
        except Exception as e:
            print(f"Connection failed: {e}")
            retry_count += 1
            if retry_count < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("Max retry attempts reached. Exiting...")
                exit()

    return engine


@lru_cache
def create_session() -> scoped_session:
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=getconn())
    )
    return Session


def get_session() -> Generator[scoped_session, None, None]:
    Session = create_session()
    try:
        yield Session
    finally:
        Session.remove()
