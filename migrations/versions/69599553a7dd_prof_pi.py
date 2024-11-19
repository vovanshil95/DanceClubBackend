"""prof_pi

Revision ID: 69599553a7dd
Revises: 07538d0e031c
Create Date: 2024-11-19 14:13:27.258389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69599553a7dd'
down_revision = '07538d0e031c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile_picture',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('data', sa.LargeBinary(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['person.person_id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile_picture')
    # ### end Alembic commands ###