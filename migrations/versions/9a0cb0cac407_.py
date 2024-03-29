"""empty message

Revision ID: 9a0cb0cac407
Revises: 5c9f56c52cc5
Create Date: 2024-03-17 20:51:29.881933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a0cb0cac407'
down_revision = '5c9f56c52cc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('user_character_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('user_planet_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'favorite', ['favorite_id'], ['id'])
        batch_op.drop_column('character_id')
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('user_planet_id_fkey', 'planet', ['planet_id'], ['id'])
        batch_op.create_foreign_key('user_character_id_fkey', 'character', ['character_id'], ['id'])
        batch_op.drop_column('favorite_id')

    # ### end Alembic commands ###
