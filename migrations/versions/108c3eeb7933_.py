"""empty message

Revision ID: 108c3eeb7933
Revises: 225eb9d17adc
Create Date: 2020-08-29 23:09:55.081059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '108c3eeb7933'
down_revision = '225eb9d17adc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tweetId', sa.Integer(), nullable=False),
    sa.Column('likedUserId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['likedUserId'], ['users.id'], ),
    sa.ForeignKeyConstraint(['tweetId'], ['tweets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###
