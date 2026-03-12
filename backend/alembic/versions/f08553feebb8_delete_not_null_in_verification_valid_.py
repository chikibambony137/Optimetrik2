"""delete NOT NULL in verification - valid_until

Revision ID: f08553feebb8
Revises: 9b64ba7041d6
Create Date: 2026-03-12 11:54:36.119213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f08553feebb8'
down_revision: Union[str, Sequence[str], None] = '9b64ba7041d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
