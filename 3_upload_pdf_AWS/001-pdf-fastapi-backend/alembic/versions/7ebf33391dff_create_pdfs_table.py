"""create pdfs table

Revision ID: 7ebf33391dff
Revises: 30a84d438097
Create Date: 2024-10-02 17:22:21.993405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ebf33391dff'
down_revision: Union[str, None] = '30a84d438097'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
