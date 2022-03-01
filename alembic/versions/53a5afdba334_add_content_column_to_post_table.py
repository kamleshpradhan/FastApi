"""add content column to post table

Revision ID: 53a5afdba334
Revises: 30228ea936b9
Create Date: 2022-03-01 12:02:39.312440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53a5afdba334'
down_revision = '30228ea936b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column('content',sa.String,nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
