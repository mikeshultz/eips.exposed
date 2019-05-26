"""create fti

Revision ID: e8a8b2096cfe
Revises: 3c301f386faa
Create Date: 2019-05-26 13:06:39.937517

"""
from sqlalchemy import text, Column
from sqlalchemy_utils.types.ts_vector import TSVectorType
from alembic import op


# revision identifiers, used by Alembic.
revision = 'e8a8b2096cfe'
down_revision = '3c301f386faa'
branch_labels = None
depends_on = None


def upgrade():
    # EIP Search
    op.add_column('eip', Column(
        'search_vector',
        TSVectorType,
    ))
    op.create_index(
        'idx_eip_search_tsv',
        'eip',
        ['search_vector'],
        unique=False,
        postgresql_using='gin'
    )
    op.execute("""
        CREATE TRIGGER update_eip_tsv
        BEFORE INSERT OR UPDATE ON eip FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(search_vector, 'pg_catalog.english', title, full_text);
    """)

    # Commit search
    op.add_column('commit', Column(
        'search_vector',
        TSVectorType,
    ))
    op.create_index(
        'idx_commit_search_tsv',
        'commit',
        ['search_vector'],
        unique=False,
        postgresql_using='gin'
    )
    op.execute("""
        CREATE TRIGGER update_commit_tsv
        BEFORE INSERT OR UPDATE ON commit FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(search_vector, 'pg_catalog.english', committer, message);
    """)


def downgrade():
    op.execute("DROP TRIGGER update_commit_tsv;")
    op.drop_index('idx_commit_search_tsv', 'commit')
    op.drop_column('commit', 'search_vector')

    op.execute("DROP TRIGGER update_eip_tsv;")
    op.drop_index('idx_eip_search_tsv', 'eip')
    op.drop_column('eip', 'search_vector')
