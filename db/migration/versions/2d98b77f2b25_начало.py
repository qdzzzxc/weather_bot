"""начало

Revision ID: 2d98b77f2b25
Revises: 
Create Date: 2023-08-17 00:36:48.476995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d98b77f2b25'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('city', sa.VARCHAR(length=32), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('city'),
    sa.UniqueConstraint('city')
    )
    op.create_table('users',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('last_city', sa.VARCHAR(length=256), nullable=True),
    sa.Column('user', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('user'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('weather',
    sa.Column('city_name', sa.VARCHAR(length=32), nullable=False),
    sa.Column('now', sa.Integer(), nullable=True),
    sa.Column('feels', sa.Integer(), nullable=True),
    sa.Column('type_', sa.VARCHAR(length=32), nullable=True),
    sa.Column('rain', sa.Integer(), nullable=True),
    sa.Column('day_1', sa.Integer(), nullable=True),
    sa.Column('day_2', sa.Integer(), nullable=True),
    sa.Column('day_3', sa.Integer(), nullable=True),
    sa.Column('day_4', sa.Integer(), nullable=True),
    sa.Column('day_5', sa.Integer(), nullable=True),
    sa.Column('day_6', sa.Integer(), nullable=True),
    sa.Column('day_7', sa.Integer(), nullable=True),
    sa.Column('day_8', sa.Integer(), nullable=True),
    sa.Column('day_9', sa.Integer(), nullable=True),
    sa.Column('day_10', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_name'], ['cities.city'], ),
    sa.PrimaryKeyConstraint('city_name'),
    sa.UniqueConstraint('city_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weather')
    op.drop_table('users')
    op.drop_table('cities')
    # ### end Alembic commands ###
