"""Added genre column to Book

Revision ID: 87bad795f4c9
Revises: 9a4aa1dca3db
Create Date: 2023-11-29 23:03:54.471673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87bad795f4c9'
down_revision: Union[str, None] = '9a4aa1dca3db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
