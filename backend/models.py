# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer, LargeBinary, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = 'Account'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    profilPicture = Column(LargeBinary)
    isManager = Column(Integer, nullable=False)
    creationDate = Column(Date)


class Anime(Base):
    __tablename__ = 'Anime'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    posterImg = Column(LargeBinary, nullable=False)
    description = Column(Text, nullable=False)


class Author(Base):
    __tablename__ = 'Author'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    posterImg = Column(LargeBinary, nullable=False)

    Music = relationship('Music', secondary='Chante')


t_Chante = Table(
    'Chante', metadata,
    Column('id_Music', ForeignKey('Music.id'),
           primary_key=True, nullable=False),
    Column('id_Author', ForeignKey('Author.id'),
           primary_key=True, nullable=False, index=True)
)


class Music(Base):
    __tablename__ = 'Music'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False)
    posterImg = Column(LargeBinary)
    releaseDate = Column(Date, nullable=False)
    id_Anime = Column(ForeignKey('Anime.id'), nullable=False, index=True)
    id_Type = Column(ForeignKey('Type.id'), nullable=False, index=True)

    Anime = relationship('Anime')
    Type = relationship('Type')


class Review(Base):
    __tablename__ = 'Review'

    id = Column(BigInteger, primary_key=True)
    noteVisual = Column(Integer, nullable=False)
    noteMusic = Column(Integer, nullable=False)
    description = Column(Text)
    creationDate = Column(Date, nullable=False)
    id_Music = Column(ForeignKey('Music.id'), nullable=False, index=True)
    id_Account = Column(ForeignKey('Account.id'), nullable=False, index=True)

    Account = relationship('Account')
    Music = relationship('Music')


class Type(Base):
    __tablename__ = 'Type'

    id = Column(BigInteger, primary_key=True)
    typeName = Column(String(250), nullable=False, unique=True)
