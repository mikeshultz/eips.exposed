"""create commit table

Revision ID: 7857e9131ddb
Revises: 4a09f47e77ff
Create Date: 2019-05-18 14:48:47.050917

"""
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from alembic import op


# revision identifiers, used by Alembic.
revision = '7857e9131ddb'
down_revision = '4a09f47e77ff'
branch_labels = None
depends_on = None
commit_table_name = 'commit'
eip_commit_table_name = 'eip_commit'


def upgrade():
    op.create_table(
        commit_table_name,
        Column('commit_hash', String(40), primary_key=True),
        Column('committer', String(), nullable=False),
        Column('committed_date', DateTime(), nullable=False),
        Column('message', Text()),
    )
    op.create_table(
        eip_commit_table_name,
        Column('eip_commit_id', Integer, primary_key=True),
        Column('commit_hash', String(40), ForeignKey('commit.commit_hash'), nullable=False),
        Column('eip_id', Integer, ForeignKey('eip.eip_id'), nullable=False),
    )


def downgrade():
    op.drop_table(commit_table_name)
