"""create tag table

Revision ID: 3c301f386faa
Revises: 7857e9131ddb
Create Date: 2019-05-19 10:14:41.526028

"""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from alembic import op


# revision identifiers, used by Alembic.
revision = '3c301f386faa'
down_revision = '7857e9131ddb'
branch_labels = None
depends_on = None
tag_table_name = 'tag'
eip_tag_table_name = 'eip_tag'


def upgrade():
    op.create_table(
        tag_table_name,
        Column('tag_name', String(), primary_key=True),
        Column('active', Boolean(), default=True),
    )
    op.create_table(
        eip_tag_table_name,
        Column('eip_tag_id', Integer, primary_key=True),
        Column('tag_name', String(40), ForeignKey('tag.tag_name'), nullable=False),
        Column('eip_id', Integer, ForeignKey('eip.eip_id'), nullable=False),
    )


def downgrade():
    op.drop_table(eip_tag_table_name)
    op.drop_table(tag_table_name)
