"""create_votes_table

Revision ID: d6cff1306f34
Revises: d35bfb39b91c
Create Date: 2024-03-17 22:09:23.920823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6cff1306f34'
down_revision: Union[str, None] = 'd35bfb39b91c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("post_id", sa.Integer, sa.ForeignKey("post.id")),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("vote_type", sa.String),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("now()"), onupdate=sa.text("now()"))
    )


def downgrade() -> None:
    op.drop_table("votes")
