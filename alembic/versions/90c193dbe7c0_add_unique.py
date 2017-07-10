"""add unique

Revision ID: 90c193dbe7c0
Revises: 7a85be37b5ce
Create Date: 2017-07-10 21:44:14.152534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90c193dbe7c0'
down_revision = '7a85be37b5ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'wootowa_cookies', ['cookie'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wootowa_cookies', type_='unique')
    # ### end Alembic commands ###
