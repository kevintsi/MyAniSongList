from typing import List
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


t_chante = Table(
    'chante', Base.metadata,
    Column('music_id', BigInteger, primary_key=True, nullable=False),
    Column('author_id', BigInteger, primary_key=True,
           nullable=False, index=True),
    ForeignKeyConstraint(['author_id'], ['author.id'], name='chante_ibfk_1'),
    ForeignKeyConstraint(['music_id'], ['music.id'], name='chante_ibfk_2'),
    Index('ix_chante_author_id', 'author_id')
)

t_favorite = Table(
    'favorite', Base.metadata,
    Column('music_id', BigInteger, primary_key=True, nullable=False),
    Column('user_id', BigInteger, primary_key=True,
           nullable=False, index=True),
    ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_ibfk_1'),
    ForeignKeyConstraint(['music_id'], ['music.id'], name='favorite_ibfk_2'),
    Index('ix_favorite_user_id', 'user_id')
)


class User(Base):

    __tablename__ = 'user'

    id = mapped_column(BigInteger, primary_key=True)
    username = mapped_column(String(250), nullable=False, unique=True)
    email = mapped_column(String(250), nullable=False, unique=True)
    password = mapped_column(String(250), nullable=False)
    is_manager = mapped_column(Integer, nullable=False, default=False)
    profile_picture = mapped_column(String(250))
    creation_date = mapped_column(DateTime)

    reviews: Mapped[List["Review"]] = relationship(
        'Review', back_populates='user')
    favorites: Mapped[List["Music"]] = relationship(
        'Music', secondary=t_favorite)

    def __repr__(self):
        return f"User({self.id},{self.username},{self.email}, {self.creation_date}, {self.profile_picture}, {self.is_manager})"


class Anime(Base):
    __tablename__ = 'anime'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String(250), nullable=False, unique=True)
    poster_img = mapped_column(String(250), nullable=False)
    description = mapped_column(Text, nullable=False)

    musics: Mapped[List["Music"]] = relationship(
        'Music', back_populates='anime')

    def __repr__(self):
        return f"Anime({self.id},{self.name},{self.poster_img}, {self.description})"


class Author(Base):
    __tablename__ = 'author'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String(250), nullable=False, unique=True)
    poster_img = mapped_column(String(250), nullable=False)
    creation_year = mapped_column(String(50), nullable=True)

    musics: Mapped[List["Music"]] = relationship(
        'Music', secondary=t_chante, back_populates='authors')

    def __repr__(self):
        return f"Author({self.id},{self.name},{self.poster_img})"


class Type(Base):
    __tablename__ = 'type'

    id = mapped_column(BigInteger, primary_key=True)
    type_name = mapped_column(String(250), nullable=False, unique=True)

    musics: Mapped[List["Music"]] = relationship(
        'Music', back_populates='type')

    def __repr__(self):
        return f"Type({self.id},{self.type_name})"


class Music(Base):
    __tablename__ = 'music'
    __table_args__ = (
        ForeignKeyConstraint(['anime_id'], ['anime.id'], name='music_ibfk_1'),
        ForeignKeyConstraint(['type_id'], ['type.id'], name='music_ibfk_2')
    )

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String(250), nullable=False, unique=True)
    release_date = mapped_column(DateTime, nullable=False)
    avg_note = mapped_column(Float, nullable=True)
    anime_id = mapped_column(BigInteger, nullable=False, index=True)
    type_id = mapped_column(BigInteger, nullable=False, index=True)
    poster_img = mapped_column(String(250))
    id_video = mapped_column(String(25))

    authors: Mapped[List["Author"]] = relationship(
        'Author', secondary=t_chante, back_populates='musics')
    anime: Mapped["Anime"] = relationship(
        'Anime', uselist=False, back_populates='musics')
    type: Mapped["Type"] = relationship(
        'Type', uselist=False, back_populates='musics')
    reviews: Mapped[List["Review"]] = relationship(
        'Review', back_populates='music')

    def __repr__(self):
        return f"Music({self.id},{self.name},{self.release_date},{self.anime_id},{self.type_id},{self.poster_img})"


class Review(Base):
    __tablename__ = 'review'
    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'], ['user.id'], name='review_ibfk_1'),
        ForeignKeyConstraint(['music_id'], ['music.id'], name='review_ibfk_2')
    )

    id = mapped_column(BigInteger, primary_key=True)
    note_visual = mapped_column(Float, nullable=False)
    note_music = mapped_column(Float, nullable=False)
    creation_date = mapped_column(DateTime, nullable=False)
    music_id = mapped_column(BigInteger, nullable=False, index=True)
    user_id = mapped_column(BigInteger, nullable=False, index=True)
    description = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(
        'User', uselist=False, back_populates='reviews')
    music: Mapped["Music"] = relationship(
        'Music', uselist=False, back_populates='reviews')

    def __repr__(self):
        return f"Review({self.id},{self.note_visual},{self.note_music},{self.creation_date},{self.music_id},{self.user_id},{self.description})"
