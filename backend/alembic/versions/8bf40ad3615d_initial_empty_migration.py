"""Initial empty migration

Revision ID: 8bf40ad3615d
Revises: b3ef6ee4910e
Create Date: 2026-03-04 10:57:04.383114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bf40ad3615d'
down_revision: Union[str, Sequence[str], None] = 'b3ef6ee4910e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
