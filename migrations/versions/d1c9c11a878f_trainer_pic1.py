"""trainer_pic1

Revision ID: d1c9c11a878f
Revises: 54031135f3da
Create Date: 2024-11-20 15:55:18.180945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1c9c11a878f'
down_revision = '54031135f3da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trainer_picture', sa.Column('trainer_id', sa.UUID(), nullable=False))
    op.drop_constraint('trainer_picture_user_id_fkey', 'trainer_picture', type_='foreignkey')
    op.create_foreign_key(None, 'trainer_picture', 'trainer', ['trainer_id'], ['trainer_id'], ondelete='cascade')
    op.drop_column('trainer_picture', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trainer_picture', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'trainer_picture', type_='foreignkey')
    op.create_foreign_key('trainer_picture_user_id_fkey', 'trainer_picture', 'trainer', ['user_id'], ['trainer_id'], ondelete='CASCADE')
    op.drop_column('trainer_picture', 'trainer_id')
    # ### end Alembic commands ###
