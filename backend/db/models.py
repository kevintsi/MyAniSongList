# coding: utf-8
from sqlalchemy import BigInteger, Float, Column, Date, ForeignKey, Integer, LargeBinary, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = 'account'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    profil_picture = Column(LargeBinary)
    is_manager = Column(Integer, nullable=False, default=False)
    creation_date = Column(Date)


class Anime(Base):
    __tablename__ = 'anime'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    poster_img = Column(LargeBinary, nullable=False)
    description = Column(Text, nullable=False)


class Author(Base):
    __tablename__ = 'author'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    poster_img = Column(LargeBinary, nullable=False)

    music = relationship('music', secondary='chante')


t_Chante = Table(
    'chante', metadata,
    Column('music_id', ForeignKey('music.id'),
           primary_key=True, nullable=False),
    Column('author_id', ForeignKey('author.id'),
           primary_key=True, nullable=False, index=True)
)


class Music(Base):
    __tablename__ = 'music'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False)
    poster_img = Column(LargeBinary)
    release_date = Column(Date, nullable=False)
    anime_id = Column(ForeignKey('anime.id'), nullable=False, index=True)
    type_id = Column(ForeignKey('type.id'), nullable=False, index=True)

    anime = relationship('anime')
    type = relationship('type')


class Review(Base):
    __tablename__ = 'review'

    id = Column(BigInteger, primary_key=True)
    note_visual = Column(Float, nullable=False)
    note_music = Column(Float, nullable=False)
    description = Column(Text)
    creation_date = Column(Date, nullable=False)
    music_id = Column(ForeignKey('music.id'), nullable=False, index=True)
    account_id = Column(ForeignKey('account.id'), nullable=False, index=True)

    account = relationship('account')
    music = relationship('music')


class Type(Base):
    __tablename__ = 'type'

    id = Column(BigInteger, primary_key=True)
    type_name = Column(String(250), nullable=False, unique=True)
