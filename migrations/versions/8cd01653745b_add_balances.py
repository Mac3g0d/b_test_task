"""'add_balances'

Revision ID: 8cd01653745b
Revises: f493877df7d1
Create Date: 2023-02-08 02:38:21.041295

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel  # noqa: F401


# revision identifiers, used by Alembic.
revision = '8cd01653745b'
down_revision = 'f493877df7d1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('total_balance', sa.Numeric(), nullable=False))
    op.add_column('customeraccount', sa.Column('balance', sa.Numeric(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customeraccount', 'balance')
    op.drop_column('customer', 'total_balance')
    # ### end Alembic commands ###
