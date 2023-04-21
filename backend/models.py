from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BLOB, Date
from sqlalchemy.orm import relationship

from .database import Base


class Account(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=True)
    email = Column(String)
    profil_picture = Column(BLOB)
    is_manager = Column(Boolean)
    creation_date = Column(Date)
