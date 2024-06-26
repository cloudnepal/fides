"""Remove user:reset-password scope

Revision ID: 7e218e880eaf
Revises: d6c6c6555c86
Create Date: 2023-01-25 19:16:19.950294

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7e218e880eaf"
down_revision = "d6c6c6555c86"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE fidesuserpermissions SET scopes = array_remove(scopes, 'user:reset-password')"
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # TODO: how should we do this downgrade?
    pass
    # ### end Alembic commands ###
