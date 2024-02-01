"""empty message

Revision ID: e6232a32349e
Revises: 5404a8799271
Create Date: 2024-02-01 16:54:20.743343

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e6232a32349e'
down_revision = '5404a8799271'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_people', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('favorite')

    with op.batch_alter_table('favorite_planet', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
        batch_op.drop_column('favorite')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite_planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))

    with op.batch_alter_table('favorite_people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
