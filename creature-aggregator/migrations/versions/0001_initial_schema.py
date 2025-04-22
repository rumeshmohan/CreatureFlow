"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2025-04-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'pokemon',
        sa.Column('id',      sa.Integer, primary_key=True),
        sa.Column('name',    sa.Text,    nullable=False),
        sa.Column('species', sa.Text),
        sa.Column('power',   sa.Integer),
    )
    op.create_table(
        'rick_morty_char',
        sa.Column('id',      sa.Integer, primary_key=True),
        sa.Column('name',    sa.Text,    nullable=False),
        sa.Column('status',  sa.Text),
        sa.Column('species', sa.Text),
    )

def downgrade():
    op.drop_table('rick_morty_char')
    op.drop_table('pokemon')
