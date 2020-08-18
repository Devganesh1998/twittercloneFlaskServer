"""empty message

Revision ID: ddd69e0393d2
Revises: fefa2a6c2707
Create Date: 2020-08-18 18:01:26.043045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddd69e0393d2'
down_revision = 'fefa2a6c2707'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parentId', sa.Integer(), nullable=True),
    sa.Column('follower', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follower'], ['users.id'], ),
    sa.ForeignKeyConstraint(['parentId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tweets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('description', sa.Text(length=4294000000), nullable=True),
    sa.Column('likes', sa.Integer(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('createdAt', sa.DateTime(), nullable=True),
    sa.Column('updatedAt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweets')
    op.drop_table('followers')
    # ### end Alembic commands ###
