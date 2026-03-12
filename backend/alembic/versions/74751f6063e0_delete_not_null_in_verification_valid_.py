"""delete NOT NULL in verification - valid_until

Revision ID: 74751f6063e0
Revises: f08553feebb8
Create Date: 2026-03-12 11:55:03.306053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74751f6063e0'
down_revision: Union[str, Sequence[str], None] = 'f08553feebb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
