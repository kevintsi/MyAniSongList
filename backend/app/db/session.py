from functools import lru_cache
from typing import Generator

from app.config import get_settings
from pymysql import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    get_settings().database_url, pool_pre_ping=True, pool_recycle=3600
)


@lru_cache
def create_session() -> scoped_session:
    """
    Create and return the scoped_session

    Returns:
        scoped_session: Session
    """
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    return Session


async def get_session() -> Generator[scoped_session, None, None]:
    """
    Get session

    Yields:
        Generator[scoped_session, None, None]: Session
    """
    print("Create the session")
    Session = create_session()
    try:
        Session.rollback()
        yield Session
    except OperationalError as e:
        print(f"Error occured, rollback : {e}")
        Session.rollback()
    finally:
        print("Close the session")
        Session.close()
