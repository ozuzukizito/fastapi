"""create posts table

Revision ID: 1501fff028af
Revises: 
Create Date: 2022-11-25 08:46:05.733716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1501fff028af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=True, 
                    primary_key=True), sa.Column('title', sa.String(), nullable=True))
    pass


def downgrade():
    op.drop_table('posts')
    pass
