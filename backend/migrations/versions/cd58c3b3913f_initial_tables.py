"""initial tables

Revision ID: cd58c3b3913f
Revises: 
Create Date: 2023-06-12 14:58:28.770927

"""
from datetime import datetime
import os
from alembic import op
import sqlalchemy as sa

from app.utils import get_password_hash


# revision identifiers, used by Alembic.
revision = 'cd58c3b3913f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supported_language',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('code', sa.String(length=10), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('code'),
                    )

    op.create_table('anime',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('poster_img', sa.String(
                        length=250), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    )

    op.create_table('anime_translation',
                    sa.Column('id_anime', sa.Integer(), nullable=False),
                    sa.Column('id_language', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=250), nullable=False),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['id_anime'], ['anime.id'], name='anime_translation_ibfk_1'),
                    sa.ForeignKeyConstraint(
                        ['id_language'], ['supported_language.id'], name='anime_translation_ibfk_2'),
                    sa.PrimaryKeyConstraint('id_anime', 'id_language')
                    )

    op.create_index('ix_anime_translation_id_anime', 'anime_translation',
                    ['id_anime'], unique=False)
    op.create_index('ix_anime_translation_id_language', 'anime_translation',
                    ['id_language'], unique=False)

    op.create_table('author',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=250), nullable=False),
                    sa.Column('poster_img', sa.String(
                        length=250), nullable=False),
                    sa.Column('creation_year', sa.String(
                        length=50), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )

    op.create_table('type',
                    sa.Column('id', sa.Integer(),
                              nullable=False),
                    sa.Column('name', sa.String(length=250), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    )
    op.create_table('type_translation',
                    sa.Column('id_type', sa.Integer(),
                              nullable=False),
                    sa.Column('id_language',
                              sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(
                        length=250, collation='utf8_unicode_ci'), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['id_type'], ['type.id'], name='type_translation_ibfk_1'),
                    sa.ForeignKeyConstraint(
                        ['id_language'], ['supported_language.id'], name='type_translation_ibfk_2'),
                    sa.PrimaryKeyConstraint('id_type', 'id_language')
                    )

    op.create_index('ix_type_translation_id_type', 'type_translation',
                    ['id_type'], unique=False)
    op.create_index('ix_type_translation_id_language', 'type_translation',
                    ['id_language'], unique=False)

    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(
                        length=250), nullable=False),
                    sa.Column('email', sa.String(length=250), nullable=False),
                    sa.Column('password', sa.String(
                        length=250), nullable=False),
                    sa.Column('is_manager', sa.Integer(), nullable=False),
                    sa.Column('profile_picture', sa.String(
                        length=250), nullable=True),
                    sa.Column('creation_date', sa.DateTime(), nullable=False,
                              server_default=sa.text("CURRENT_TIMESTAMP")),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )

    op.execute(
        f"INSERT INTO user (username, email, password, is_manager, profile_picture) VALUES ('{os.getenv('USERNAME_ADMIN')}', 'admin@gmail.com', '{get_password_hash(os.getenv('PASSWORD_ADMIN'))}', 1, null);")

    op.create_table('music',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=250), nullable=False),
                    sa.Column('release_date', sa.DateTime(), nullable=False),
                    sa.Column('avg_note', sa.Float(), nullable=True),
                    sa.Column('anime_id', sa.Integer(), nullable=False),
                    sa.Column('type_id', sa.Integer(), nullable=False),
                    sa.Column('poster_img', sa.String(
                        length=250), nullable=True),
                    sa.Column('id_video', sa.String(
                        length=25), nullable=True),
                    sa.Column('creation_date', sa.DateTime(
                    ), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
                    sa.ForeignKeyConstraint(
                        ['anime_id'], ['anime.id'], name='music_ibfk_1'),
                    sa.ForeignKeyConstraint(
                        ['type_id'], ['type.id'], name='music_ibfk_2'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )

    op.create_index(op.f('ix_music_anime_id'), 'music',
                    ['anime_id'], unique=False)
    op.create_index(op.f('ix_music_type_id'), 'music',
                    ['type_id'], unique=False)

    op.create_table('chante',
                    sa.Column('music_id', sa.Integer(), nullable=False),
                    sa.Column('author_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['author_id'], ['author.id'], name='chante_ibfk_1',  ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(
                        ['music_id'], ['music.id'], name='chante_ibfk_2',  ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('music_id', 'author_id')
                    )

    op.create_index('ix_chante_author_id', 'chante',
                    ['author_id'], unique=False)

    op.create_table('review',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('note_visual', sa.Float(), nullable=False),
                    sa.Column('note_music', sa.Float(), nullable=False),
                    sa.Column('creation_date', sa.DateTime(), nullable=False),
                    sa.Column('music_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['music_id'], ['music.id'], name='review_ibfk_2', ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['user.id'], name='review_ibfk_1',  ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_index(op.f('ix_review_music_id'),
                    'review', ['music_id'], unique=False)
    op.create_index(op.f('ix_review_user_id'),
                    'review', ['user_id'], unique=False)

    op.create_table('favorite',
                    sa.Column('music_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['music_id'], ['music.id'], name='favorite_ibfk_2', ondelete="CASCADE"),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['user.id'], name='favorite_ibfk_1', ondelete="CASCADE"),
                    sa.PrimaryKeyConstraint('music_id', 'user_id')
                    )

    op.create_index('ix_favorite_user_id', 'favorite',
                    ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("review_ibfk_2", "review", type_="foreignkey")
    op.drop_constraint("review_ibfk_1", "review", type_="foreignkey")
    op.drop_index(op.f('ix_review_user_id'), table_name='review')
    op.drop_index(op.f('ix_review_music_id'), table_name='review')
    op.drop_table('review')
    op.drop_constraint("chante_ibfk_2", "chante", type_="foreignkey")
    op.drop_constraint("chante_ibfk_1", "chante", type_="foreignkey")
    op.drop_index('ix_chante_author_id', table_name='chante')
    op.drop_table('chante')
    op.drop_constraint("music_ibfk_2", "music", type_="foreignkey")
    op.drop_constraint("music_ibfk_1", "music", type_="foreignkey")
    op.drop_index(op.f('ix_music_type_id'), table_name='music')
    op.drop_index(op.f('ix_music_anime_id'), table_name='music')
    op.drop_constraint("favorite_ibfk_1", "favorite", type_="foreignkey")
    op.drop_constraint("favorite_ibfk_2", "favorite", type_="foreignkey")
    op.drop_index('ix_favorite_user_id', table_name='favorite')
    op.drop_index('ix_anime_translation_anime_id',
                  table_name='anime_translation')
    op.drop_index('ix_anime_translation_language_id',
                  table_name='anime_translation')
    op.drop_index('ix_type_translation_id_type', table_name='type_translation')
    op.drop_index('ix_type_translation_id_language',
                  table_name='type_translation')
    op.drop_constraint('anime_translation_ibfk_1',
                       table_name="anime_translation", type_="foreignkey")
    op.drop_constraint('anime_translation_ibfk_2',
                       table_name="anime", type_="foreignkey")
    op.drop_constraint('type_translation_ibfk_1',
                       table_name="type_translation", type_="foreignkey")
    op.drop_constraint('type_translation_ifbk_2',
                       table_name="type_translation", type_="foreignkey")
    op.drop_table('favorite')
    op.drop_table('music')
    op.drop_table('user')
    op.drop_table('supported_language')
    op.drop_table('type_translation')
    op.drop_table('type')
    op.drop_table('author')
    op.drop_table('anime_translation')
    op.drop_table('anime')
    # ### end Alembic commands ###
