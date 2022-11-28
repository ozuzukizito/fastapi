"""add content to posts table

Revision ID: 87f33b012345
Revises: 49589d6c8ec6
Create Date: 2022-11-27 10:12:10.958669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87f33b012345'
down_revision = '49589d6c8ec6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
