"""create guild table

Revision ID: 851d11b8a33e
Revises: 
Create Date: 2021-01-18 13:02:51.910663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "851d11b8a33e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "guild",
        sa.Column("id", sa.BIGINT, primary_key=True),
        sa.Column("prefix", sa.Unicode(200)),
        sa.Column("locale", sa.Unicode(200)),
    )


def downgrade():
    op.drop_table("guild")
