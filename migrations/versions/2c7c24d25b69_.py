"""empty message

Revision ID: 2c7c24d25b69
Revises: 4cfc9cf622fa
Create Date: 2023-09-18 16:22:06.155397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c7c24d25b69'
down_revision = '4cfc9cf622fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('budgets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('budget', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('budgets')
    # ### end Alembic commands ###
