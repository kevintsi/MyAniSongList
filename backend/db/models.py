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
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
metadata = Base.metadata


t_chante = Table(
    'chante', metadata,
    Column('music_id', BigInteger, primary_key=True, nullable=False),
    Column('author_id', BigInteger, primary_key=True,
           nullable=False, index=True),
    ForeignKeyConstraint(['author_id'], ['author.id'], name='chante_ibfk_1'),
    ForeignKeyConstraint(['music_id'], ['music.id'], name='chante_ibfk_2'),
    Index('ix_chante_author_id', 'author_id')
)


class User(Base):

    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)
    is_manager = Column(Integer, nullable=False, default=False)
    profile_picture = Column(String(250))
    creation_date = Column(DateTime)

    reviews: list = relationship('Review', back_populates='users')

    def __repr__(self):
        return f"User({self.id},{self.username},{self.email}, {self.creation_date}, {self.profile_picture}, {self.is_manager})"


class Anime(Base):
    __tablename__ = 'anime'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    poster_img = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)

    musics: list = relationship('Music', back_populates='anime')

    def __repr__(self):
        return f"Anime({self.id},{self.name},{self.poster_img}, {self.description})"


class Author(Base):
    __tablename__ = 'author'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    poster_img = Column(String(250), nullable=False)
    creation_year = Column(String(50), nullable=True)

    musics: list = relationship(
        'Music', secondary=t_chante, back_populates='authors')

    def __repr__(self):
        return f"Author({self.id},{self.name},{self.poster_img})"


class Type(Base):
    __tablename__ = 'type'

    id = Column(BigInteger, primary_key=True)
    type_name = Column(String(250), nullable=False, unique=True)

    musics = relationship('Music', back_populates='type')

    def __repr__(self):
        return f"Type({self.id},{self.type_name})"


class Music(Base):
    __tablename__ = 'music'
    __table_args__ = (
        ForeignKeyConstraint(['anime_id'], ['anime.id'], name='music_ibfk_1'),
        ForeignKeyConstraint(['type_id'], ['type.id'], name='music_ibfk_2')
    )

    id = Column(BigInteger, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    release_date = Column(DateTime, nullable=False)
    anime_id = Column(BigInteger, nullable=False, index=True)
    type_id = Column(BigInteger, nullable=False, index=True)
    poster_img = Column(String(250))

    authors = relationship(
        'Author', secondary=t_chante, back_populates='musics')
    anime = relationship('Anime', uselist=False, back_populates='musics')
    type = relationship('Type', uselist=False, back_populates='musics')
    reviews = relationship('Review', back_populates='musics')

    def __repr__(self):
        return f"Music({self.id},{self.name},{self.release_date},{self.anime_id},{self.type_id},{self.poster_img})"


class Review(Base):
    __tablename__ = 'review'
    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'], ['user.id'], name='review_ibfk_1'),
        ForeignKeyConstraint(['music_id'], ['music.id'], name='review_ibfk_2')
    )

    id = Column(BigInteger, primary_key=True)
    note_visual = Column(Float, nullable=False)
    note_music = Column(Float, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    music_id = Column(BigInteger, nullable=False, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    description = Column(Text)

    users = relationship('User', back_populates='reviews')
    musics = relationship('Music', back_populates='reviews')

    def __repr__(self):
        return f"Review({self.id},{self.note_visual},{self.note_music},{self.creation_date},{self.music_id},{self.user_id},{self.description})"
