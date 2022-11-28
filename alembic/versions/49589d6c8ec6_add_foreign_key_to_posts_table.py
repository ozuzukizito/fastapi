"""add foreign-key to posts table

Revision ID: 49589d6c8ec6
Revises: a66c441e5668
Create Date: 2022-11-27 08:57:09.015735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49589d6c8ec6'
down_revision = 'a66c441e5668'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk',source_table="posts", referent_table="users",
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
