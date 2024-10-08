"""Initial migration

Revision ID: dc84a341233c
Revises: 
Create Date: 2024-07-25 11:13:33.125884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc84a341233c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievement',
    sa.Column('achievement_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('badge_image', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('achievement_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('deck',
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('shared', sa.Boolean(), nullable=True),
    sa.Column('review_start_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('deck_id')
    )
    op.create_table('login_event',
    sa.Column('login_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('login_id')
    )
    op.create_table('user_achievement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('achievement_id', sa.Integer(), nullable=False),
    sa.Column('date_earned', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['achievement_id'], ['achievement.achievement_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('front', sa.String(length=255), nullable=False),
    sa.Column('back', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('next_review_date', sa.DateTime(), nullable=True),
    sa.Column('deck_id', sa.Integer(), nullable=False),
    sa.Column('box', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['deck_id'], ['deck.deck_id'], ),
    sa.PrimaryKeyConstraint('card_id')
    )
    op.create_table('review_outcome',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('correct', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('session_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['card.card_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review_outcome')
    op.drop_table('card')
    op.drop_table('user_achievement')
    op.drop_table('login_event')
    op.drop_table('deck')
    op.drop_table('user')
    op.drop_table('achievement')
    # ### end Alembic commands ###
