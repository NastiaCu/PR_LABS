"""Initial migration.

Revision ID: 543bf66b9a26
Revises: 
Create Date: 2023-10-19 02:11:49.539871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '543bf66b9a26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scooters')
    with op.batch_alter_table('electro_scooter', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('battery_level',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
        batch_op.drop_column('primary_key')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('electro_scooter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('primary_key', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.alter_column('battery_level',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=80),
               nullable=True)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)

    op.create_table('scooters',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('battery_level', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###
