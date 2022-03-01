"""add foreign key to posts table

Revision ID: 1b845e807042
Revises: 0fd34d418794
Create Date: 2022-03-01 12:26:11.898035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b845e807042'
down_revision = '0fd34d418794'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table ='posts', referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_tk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
