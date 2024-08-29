"""Added target column to Achievements model to facilitate progress bars

Revision ID: fdd7f8550892
Revises: dc84a341233c
Create Date: 2024-07-25 15:23:18.244978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdd7f8550892'
down_revision = 'dc84a341233c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('achievement', schema=None) as batch_op:
        batch_op.add_column(sa.Column('target', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('achievement', schema=None) as batch_op:
        batch_op.drop_column('target')

    # ### end Alembic commands ###