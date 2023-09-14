from contextlib import contextmanager
from functools import lru_cache
import time
from typing import Generator

from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker, Session

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


engine = create_engine(get_settings().database_url,
                       pool_pre_ping=True, pool_recycle=1800)


@lru_cache
def create_session() -> scoped_session:
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine))

    return Session


def get_session() -> Generator[scoped_session, None, None]:
    Session = create_session()
    try:
        yield Session
    except Exception as e:
        print("Error occured, rollback")
        print(e)
        Session.rollback()
    finally:
        print("Remove the session")
        Session.remove()
