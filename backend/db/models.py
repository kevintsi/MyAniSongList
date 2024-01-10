from datetime import datetime
from typing import List
from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, column_property


class Base(DeclarativeBase):
    pass


class Chante(Base):

    __tablename__ = 'chante'

    music_id = mapped_column(ForeignKey('music.id', ondelete="CASCADE"),
                             primary_key=True)
    author_id = mapped_column(ForeignKey('author.id', ondelete="CASCADE"),
                              nullable=False, unique=True, index=True)

    author: Mapped["Author"] = relationship(
        uselist=False, back_populates="chantes")
    music: Mapped["Music"] = relationship(
        uselist=False, back_populates="chantes")


class Favorite(Base):

    __tablename__ = 'favorite'

    music_id = mapped_column(ForeignKey('music.id', ondelete="CASCADE"),
                             primary_key=True)
    user_id = mapped_column(ForeignKey('user.id'),
                            nullable=False, unique=True, index=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    music: Mapped["Music"] = relationship(back_populates="favorites")


class AnimeTranslation(Base):

    __tablename__ = 'anime_translation'

    id_anime = mapped_column(ForeignKey('anime.id'),
                             primary_key=True, index=True)
    id_language = mapped_column(ForeignKey('supported_language.id', ondelete="CASCADE"), primary_key=True,
                                nullable=False, unique=True, index=True)
    name = mapped_column(String(length=250), nullable=False)
    description = mapped_column(Text(), nullable=False)

    anime: Mapped["Anime"] = relationship(
        'Anime', back_populates="anime_translations")
    language: Mapped["Language"] = relationship(
        back_populates="anime_translations")

    def __repr__(self):
        return f"AnimeTranslation({self.name},{self.description})"


class Anime(Base):
    __tablename__ = 'anime'

    id = mapped_column(BigInteger, primary_key=True)
    poster_img = mapped_column(String(250), nullable=False)

    anime_translations: Mapped[List[AnimeTranslation]
                               ] = relationship(back_populates='anime')
    musics: Mapped[List["Music"]] = relationship(back_populates='anime')

    def __repr__(self):
        return f"Anime({self.id},{self.poster_img})"


class TypeTranslation(Base):

    __tablename__ = 'type_translation'

    id_type = mapped_column(ForeignKey('type.id'),
                            primary_key=True, index=True)
    id_language = mapped_column(ForeignKey('supported_language.id', ondelete="CASCADE"),
                                nullable=False, unique=True, index=True)
    name = mapped_column(String(length=250), nullable=False)

    type: Mapped["Type"] = relationship(back_populates="type_translations")
    language: Mapped["Language"] = relationship(
        back_populates="type_translations")


class Type(Base):
    __tablename__ = 'type'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String(length=250), nullable=False)

    type_translations: Mapped[List[TypeTranslation]] = relationship(
        back_populates='type')
    musics: Mapped[List["Music"]] = relationship(back_populates='type')

    def __repr__(self):
        return f"Type({self.id})"


class Language(Base):

    __tablename__ = 'supported_language'

    id = mapped_column(BigInteger, primary_key=True)
    code = mapped_column(String(10), nullable=False, unique=True)

    anime_translations: Mapped[List[AnimeTranslation]
                               ] = relationship(back_populates="language", cascade="all, delete")
    type_translations: Mapped[List[TypeTranslation]
                              ] = relationship(back_populates="language",  cascade="all, delete")

    def __repr__(self):
        return f"Language({self.id, self.code})"


class User(Base):

    __tablename__ = 'user'

    id = mapped_column(BigInteger, primary_key=True)
    username = mapped_column(String(250), nullable=False, unique=True)
    email = mapped_column(String(250), nullable=False, unique=True)
    password = mapped_column(String(250), nullable=False)
    is_manager = mapped_column(Integer, nullable=False, default=False)
    profile_picture = mapped_column(String(250))
    creation_date = mapped_column(
        DateTime, nullable=False,  default=func.now())

    reviews: Mapped[List["Review"]] = relationship(
        back_populates='user', cascade="all, delete")
    favorites: Mapped[List[Favorite]] = relationship(
        cascade="all, delete", back_populates="user")

    def __repr__(self):
        return f"User({self.id},{self.username},{self.email}, {self.creation_date}, {self.profile_picture}, {self.is_manager})"


class Author(Base):
    __tablename__ = 'author'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String(250), nullable=False, unique=True)
    poster_img = mapped_column(String(250), nullable=False)
    creation_year = mapped_column(String(50), nullable=True)

    chantes: Mapped[List[Chante]] = relationship(
        back_populates="author", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f"Author({self.id},{self.name},{self.poster_img})"


class Music(Base):
    __tablename__ = 'music'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String(250), nullable=False, unique=True)
    release_date = mapped_column(DateTime, nullable=False)
    avg_note = mapped_column(Float, nullable=True)
    anime_id = mapped_column(ForeignKey('anime.id'),
                             nullable=False, index=True)
    type_id = mapped_column(ForeignKey('type.id'), nullable=False, index=True)
    poster_img = mapped_column(String(250))
    id_video = mapped_column(String(25))
    creation_date = mapped_column(DateTime, nullable=False, default=func.now())

    anime: Mapped["Anime"] = relationship(
        'Anime', back_populates='musics',)
    type: Mapped["Type"] = relationship(
        'Type', back_populates='musics')
    reviews: Mapped[List["Review"]] = relationship(
        back_populates='music', cascade="all, delete",
        passive_deletes=True,)
    favorites: Mapped[List[Favorite]] = relationship(
        back_populates="music", cascade="all, delete",
        passive_deletes=True,)

    chantes: Mapped[List[Chante]] = relationship(
        back_populates="music", cascade="all, delete",
        passive_deletes=True,)

    def __repr__(self):
        return f"Music({self.id},{self.name},{self.release_date},{self.anime_id},{self.type_id},{self.poster_img})"


class Review(Base):
    __tablename__ = 'review'

    id = mapped_column(BigInteger, primary_key=True)
    note_visual = mapped_column(Float, nullable=False)
    note_music = mapped_column(Float, nullable=False)
    creation_date = mapped_column(DateTime, nullable=False)
    music_id = mapped_column(ForeignKey('music.id', ondelete="CASCADE"),
                             nullable=False, index=True)
    user_id = mapped_column(ForeignKey('user.id'), nullable=False, index=True)
    description = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(
        'User', back_populates='reviews')
    music: Mapped["Music"] = relationship(
        'Music', back_populates='reviews')

    def __repr__(self):
        return f"Review({self.id},{self.note_visual},{self.note_music},{self.creation_date},{self.music_id},{self.user_id},{self.description})"
