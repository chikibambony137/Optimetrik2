"""one more migration

Revision ID: 81895beae219
Revises: 92e6b60c1f9a
Create Date: 2026-03-12 11:50:10.073803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81895beae219'
down_revision: Union[str, Sequence[str], None] = '92e6b60c1f9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
