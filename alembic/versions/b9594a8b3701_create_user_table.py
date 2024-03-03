"""create_user_table

Revision ID: b9594a8b3701
Revises: 
Create Date: 2024-03-02 16:03:29.731464

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9594a8b3701'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('username', sa.String(255), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, server_default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade() -> None:
    op.drop_table('users')
