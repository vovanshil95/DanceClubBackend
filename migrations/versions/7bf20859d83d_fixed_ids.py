"""fixed ids

Revision ID: 7bf20859d83d
Revises: 22bad8695bb4
Create Date: 2024-10-12 20:40:32.510892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bf20859d83d'
down_revision = '22bad8695bb4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('training_sign', 'training_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('training_sign', 'person_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'training_sign', 'person', ['person_id'], ['person_id'], ondelete='cascade')
    op.create_foreign_key(None, 'training_sign', 'training', ['training_id'], ['training_id'], ondelete='cascade')
    op.drop_column('training_sign', 'sign_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('training_sign', sa.Column('sign_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'training_sign', type_='foreignkey')
    op.drop_constraint(None, 'training_sign', type_='foreignkey')
    op.alter_column('training_sign', 'person_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('training_sign', 'training_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
