"""empty message

Revision ID: 3c87cd01a5fc
Revises: d48fbc930798
Create Date: 2024-08-07 10:51:42.095159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c87cd01a5fc'
down_revision = 'd48fbc930798'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('species', sa.String(length=80), nullable=False))
        batch_op.add_column(sa.Column('height', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('mass', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('hair_color', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('skin_color', sa.String(length=20), nullable=False))
        batch_op.add_column(sa.Column('homeworld', sa.String(length=80), nullable=False))
        batch_op.drop_column('eye_color')

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('diameter', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('gravity', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('orbital_period', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('population', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('rotation_period', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('surface_water', sa.String(length=120), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_column('surface_water')
        batch_op.drop_column('rotation_period')
        batch_op.drop_column('population')
        batch_op.drop_column('orbital_period')
        batch_op.drop_column('gravity')
        batch_op.drop_column('diameter')

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.add_column(sa.Column('eye_color', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
        batch_op.drop_column('homeworld')
        batch_op.drop_column('skin_color')
        batch_op.drop_column('hair_color')
        batch_op.drop_column('mass')
        batch_op.drop_column('height')
        batch_op.drop_column('species')

    # ### end Alembic commands ###
