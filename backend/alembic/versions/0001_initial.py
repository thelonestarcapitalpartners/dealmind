"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-22 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
dependencies = None


def upgrade():
    """Create tables using SQLAlchemy metadata as a pragmatic initial migration."""
    # Importing and calling init_db will create all tables defined in SQLAlchemy models
    from app.utils.database import init_db

    init_db()


def downgrade():
    """Drop tables (dangerous)"""
    from app.utils.database import drop_db

    drop_db()
