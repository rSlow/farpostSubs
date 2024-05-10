"""empty message

Revision ID: 6460b1fb3889
Revises: 2e4f68e01d8e
Create Date: 2024-05-09 23:03:00.757972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6460b1fb3889'
down_revision: Union[str, None] = '2e4f68e01d8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subscriptions', 'url',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subscriptions', 'url',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###