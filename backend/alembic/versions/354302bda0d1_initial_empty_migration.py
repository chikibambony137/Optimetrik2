"""Initial empty migration

Revision ID: 354302bda0d1
Revises: 8bf40ad3615d
Create Date: 2026-03-04 11:47:45.131741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '354302bda0d1'
down_revision: Union[str, Sequence[str], None] = '8bf40ad3615d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
