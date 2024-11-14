"""description

Revision ID: e8ad4e90ebb8
Revises: b398b4de720d
Create Date: 2024-11-11 20:18:03.708010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8ad4e90ebb8'
down_revision = 'b398b4de720d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('salt', sa.LargeBinary(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['person.person_id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('refresh_token',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_agent', sa.String(), nullable=False),
    sa.Column('exp', sa.TIMESTAMP(), nullable=False),
    sa.Column('last_use', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['person.person_id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh_token')
    op.drop_table('auth')
    # ### end Alembic commands ###
