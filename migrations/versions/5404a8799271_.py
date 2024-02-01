"""empty message

Revision ID: 5404a8799271
Revises: 3291b9932726
Create Date: 2024-02-01 16:13:09.247911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5404a8799271'
down_revision = '3291b9932726'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('specie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('homeworld_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'planet', ['homeworld_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('specie', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('homeworld_id')

    # ### end Alembic commands ###
