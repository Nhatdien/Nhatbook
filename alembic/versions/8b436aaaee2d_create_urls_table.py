"""create_urls_table

Revision ID: 8b436aaaee2d
Revises: 
Create Date: 2024-02-19 22:05:40.446761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b436aaaee2d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('long_url', sa.String(), nullable=False),
    sa.Column('short_url', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
   op.drop_table("urls")
