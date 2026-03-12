"""delete NOT NULL in verification

Revision ID: 9b64ba7041d6
Revises: 81895beae219
Create Date: 2026-03-12 11:53:36.342535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b64ba7041d6'
down_revision: Union[str, Sequence[str], None] = '81895beae219'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
