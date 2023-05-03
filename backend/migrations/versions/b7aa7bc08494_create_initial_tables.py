"""create initial tables

Revision ID: b7aa7bc08494
Revises: 
Create Date: 2023-04-25 13:59:54.059798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7aa7bc08494'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('profil_picture', sa.LargeBinary(), nullable=True),
    sa.Column('is_manager', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('anime',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('poster_img', sa.LargeBinary(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('author',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('poster_img', sa.LargeBinary(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('type',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('type_name', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_name')
    )
    op.create_table('music',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('poster_img', sa.LargeBinary(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('anime_id', sa.BigInteger(), nullable=False),
    sa.Column('type_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['anime_id'], ['anime.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_music_anime_id'), 'music', ['anime_id'], unique=False)
    op.create_index(op.f('ix_music_type_id'), 'music', ['type_id'], unique=False)
    op.create_table('chante',
    sa.Column('music_id', sa.BigInteger(), nullable=False),
    sa.Column('author_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['music_id'], ['music.id'], ),
    sa.PrimaryKeyConstraint('music_id', 'author_id')
    )
    op.create_index(op.f('ix_chante_author_id'), 'chante', ['author_id'], unique=False)
    op.create_table('review',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('note_visual', sa.Float(), nullable=False),
    sa.Column('note_music', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('creation_date', sa.Date(), nullable=False),
    sa.Column('music_id', sa.BigInteger(), nullable=False),
    sa.Column('account_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['music_id'], ['music.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_account_id'), 'review', ['account_id'], unique=False)
    op.create_index(op.f('ix_review_music_id'), 'review', ['music_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_review_music_id'), table_name='review')
    op.drop_index(op.f('ix_review_account_id'), table_name='review')
    op.drop_table('review')
    op.drop_index(op.f('ix_chante_author_id'), table_name='chante')
    op.drop_table('chante')
    op.drop_index(op.f('ix_music_type_id'), table_name='music')
    op.drop_index(op.f('ix_music_anime_id'), table_name='music')
    op.drop_table('music')
    op.drop_table('type')
    op.drop_table('author')
    op.drop_table('anime')
    op.drop_table('account')
    # ### end Alembic commands ###