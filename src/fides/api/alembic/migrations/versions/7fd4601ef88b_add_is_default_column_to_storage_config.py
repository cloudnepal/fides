"""add is_default column to storage config

Revision ID: 7fd4601ef88b
Revises: d6c6c6555c86
Create Date: 2023-01-26 14:13:22.538719

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

# revision identifiers, used by Alembic.
revision = "7fd4601ef88b"
down_revision = "392992c7733a"
branch_labels = None
depends_on = None


def upgrade():
    # schema migration - add a nullable storageconfig.is_default field. We will shortly make it non-nullable
    op.add_column("storageconfig", sa.Column("is_default", sa.Boolean(), nullable=True))
    op.create_index(
        op.f("ix_storageconfig_is_default"),
        "storageconfig",
        ["is_default"],
        unique=False,
    )
    op.create_index(
        "only_one_default_per_type",
        "storageconfig",
        ["type", "is_default"],
        unique=True,
        postgresql_where=sa.text("is_default"),
    )

    # Data migration - automatically populate storageconfig.is_default column
    bind = op.get_bind()
    existing_storageconfigs: TextClause = bind.execute(
        text("SELECT id FROM storageconfig;")
    )
    for row in existing_storageconfigs:
        update_storage_config_query: TextClause = text(
            "UPDATE storageconfig SET is_default = false WHERE id= :storageconfig_id"
        )
        bind.execute(update_storage_config_query, {"storageconfig_id": row["id"]})

    # now follow up to make it not nullable
    op.alter_column(
        "storageconfig", "is_default", existing_type=sa.Boolean(), nullable=False
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "only_one_default_per_type",
        table_name="storageconfig",
        postgresql_where=sa.text("is_default"),
    )
    op.drop_index(op.f("ix_storageconfig_is_default"), table_name="storageconfig")
    op.drop_column("storageconfig", "is_default")
    # ### end Alembic commands ###
