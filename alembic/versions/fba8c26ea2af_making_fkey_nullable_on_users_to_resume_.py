"""making fkey nullable on Users to resume_id

Revision ID: fba8c26ea2af
Revises: 12669f15331e
Create Date: 2023-05-02 19:50:03.144213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba8c26ea2af'
down_revision = '12669f15331e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
