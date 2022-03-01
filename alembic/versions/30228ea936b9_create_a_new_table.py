"""create a new table

Revision ID: 30228ea936b9
Revises: 
Create Date: 2022-03-01 11:50:08.880513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30228ea936b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable = False,primary_key = True),sa.Column('title',sa.String(), nullable=False))
    pass

    pass


def downgrade():
    op.drop_table('posts')
    pass
