"""create_post_table

Revision ID: d35bfb39b91c
Revises: b9594a8b3701
Create Date: 2024-03-03 10:06:09.782979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.mutable import MutableList


# revision identifiers, used by Alembic.
revision: str = 'd35bfb39b91c'
down_revision: Union[str, None] = 'b9594a8b3701'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "post",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("content", sa.String(), nullable=True),
        sa.Column("author_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE", onupdate="NO ACTION"),
                   nullable=False),
        
        #replied to
        sa.Column("replied_to_id", sa.Integer, sa.ForeignKey("post.id",  ondelete="CASCADE", onupdate="NO ACTION"),
                   nullable=True),

        #created and updated at
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), server_onupdate=sa.func.now()),

        #media file
        # sa.Column("media", sa.String(), nullable=True)
    )
    


def downgrade() -> None:
    op.drop_table("post")
