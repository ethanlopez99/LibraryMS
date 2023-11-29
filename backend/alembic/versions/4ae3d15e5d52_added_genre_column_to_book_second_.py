"""Added genre column to Book (second attempt)

Revision ID: 4ae3d15e5d52
Revises: 87bad795f4c9
Create Date: 2023-11-29 23:08:35.577416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ae3d15e5d52'
down_revision: Union[str, None] = '87bad795f4c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('genre', sa.String))


def downgrade() -> None:
    pass
