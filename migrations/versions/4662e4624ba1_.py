"""empty message

Revision ID: 4662e4624ba1
Revises: e455e7a3cdc6
Create Date: 2024-08-07 11:51:13.187368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4662e4624ba1'
down_revision = 'e455e7a3cdc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=200),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###