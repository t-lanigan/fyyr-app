"""empty message

Revision ID: 7789261b8e69
Revises: c086490fbb45
Create Date: 2020-04-28 14:09:22.906181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7789261b8e69'
down_revision = 'c086490fbb45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'artists', ['name'])
    op.create_unique_constraint(None, 'venues', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'venues', type_='unique')
    op.drop_constraint(None, 'artists', type_='unique')
    # ### end Alembic commands ###
