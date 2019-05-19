"""create eip table

Revision ID: 4a09f47e77ff
Revises:
Create Date: 2019-05-18 08:45:26.280668

"""
from sqlalchemy import Column, Integer, Enum, String, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from alembic import op
from eips_exposed.processor.objects import EIPType, EIPStatus, EIPCategory


# revision identifiers, used by Alembic.
revision = '4a09f47e77ff'
down_revision = None
branch_labels = None
depends_on = None
table_name = 'eip'


def upgrade():
    op.create_table(
        table_name,
        Column('eip_id', Integer(), primary_key=True),
        Column('eip_type', Enum(EIPType), nullable=False),
        Column('title', String(), nullable=False),
        Column('author', String(), nullable=False),
        Column('status', Enum(EIPStatus), nullable=False),
        Column('created', DateTime(), nullable=False),
        Column('updated', String()),
        Column('discussions_to', String()),
        Column('review_period_end', String()),
        Column('category', Enum(EIPCategory)),
        Column('requires', ARRAY(Integer)),
        Column('replaces', ARRAY(Integer)),
        Column('superseded_by', ARRAY(Integer)),
        Column('resolution', String()),
        Column('full_text', Text()),
    )


def downgrade():
    op.drop_table(table_name)
