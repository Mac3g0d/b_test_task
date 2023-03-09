"""'add_created_at'

Revision ID: 5ecd36a5cfb7
Revises: 8cd01653745b
Create Date: 2023-02-08 03:10:58.176263

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel  # noqa: F401

# revision identifiers, used by Alembic.
revision = '5ecd36a5cfb7'
down_revision = '8cd01653745b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accountoperation', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.drop_column('customer', 'total_balance')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('total_balance', sa.NUMERIC(), autoincrement=False, nullable=False))
    op.drop_column('accountoperation', 'created_at')
    # ### end Alembic commands ###
