"""add author to commit table

Revision ID: 9c40cd3c04d8
Revises: 4b68d97ca7d4
Create Date: 2019-06-02 03:28:48.279859

"""
from sqlalchemy import Column, String
from alembic import op


# revision identifiers, used by Alembic.
revision = '9c40cd3c04d8'
down_revision = '4b68d97ca7d4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('commit', Column('author', String()))


def downgrade():
    op.drop_column('commit', 'author')
