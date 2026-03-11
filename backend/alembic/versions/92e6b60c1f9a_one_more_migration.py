"""one more migration

Revision ID: 92e6b60c1f9a
Revises: 3b8ac0cf8657
Create Date: 2026-03-11 10:54:15.778223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92e6b60c1f9a'
down_revision: Union[str, Sequence[str], None] = '3b8ac0cf8657'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
