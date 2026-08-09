"""initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2026-08-09 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'trends',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('slug', sa.String(length=220), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('tldr', sa.Text(), nullable=True),
        sa.Column('why_it_matters', sa.Text(), nullable=True),
        sa.Column('momentum', sa.String(length=50), nullable=True),
        sa.Column('tech_stack', postgresql.JSONB(), nullable=True),
        sa.Column('related_trends', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_trends_id'), 'trends', ['id'], unique=False)
    op.create_index(op.f('ix_trends_slug'), 'trends', ['slug'], unique=False)

    op.create_table(
        'sources',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('trend_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('url', sa.String(length=1000), nullable=False),
        sa.Column('source_type', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['trend_id'], ['trends.id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_sources_id'), 'sources', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_sources_id'), table_name='sources')
    op.drop_table('sources')
    op.drop_index(op.f('ix_trends_slug'), table_name='trends')
    op.drop_index(op.f('ix_trends_id'), table_name='trends')
    op.drop_table('trends')
