"""remove user role

Revision ID: 35e72adbc764
Revises: 5402aa9c3631
Create Date: 2026-05-11 18:29:24.053331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35e72adbc764'
down_revision: Union[str, Sequence[str], None] = '5402aa9c3631'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "user_role")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "user_role",
            sa.String(length=20),
            nullable=False,
            server_default="investor",
        ),
    )
