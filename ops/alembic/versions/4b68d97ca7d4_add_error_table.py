"""add error table

Revision ID: 4b68d97ca7d4
Revises: e8a8b2096cfe
Create Date: 2019-05-26 20:13:47.470552

"""
from sqlalchemy import func, Column, Integer, Enum, Text, DateTime
from alembic import op
from eips_exposed.processor.objects import ErrorType


# revision identifiers, used by Alembic.
revision = '4b68d97ca7d4'
down_revision = 'e8a8b2096cfe'
branch_labels = None
depends_on = None
table_name = 'error'


def upgrade():
    op.create_table(
        table_name,
        Column('eip_id', Integer(), primary_key=True),
        Column('error_type', Enum(ErrorType), nullable=False),
        Column('when', DateTime, server_default=func.current_timestamp()),
        Column('message', Text),
    )


def downgrade():
    op.drop_table(table_name)
