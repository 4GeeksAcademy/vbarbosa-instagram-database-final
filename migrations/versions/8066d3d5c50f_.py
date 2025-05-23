"""empty message

Revision ID: 8066d3d5c50f
Revises: a6157f7264df
Create Date: 2025-05-09 20:53:34.656720

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8066d3d5c50f'
down_revision = "a6157f7264df"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    media_type_enum = postgresql.ENUM('IMAGE', 'VIDEO', 'AUDIO', name='mediatype')
    media_type_enum.create(op.get_bind())

    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.alter_column('type_media',
            existing_type=sa.VARCHAR(length=50),
            type_=sa.Enum('IMAGE', 'VIDEO', 'AUDIO', name='mediatype'),
            existing_nullable=False,
            postgresql_using='type_media::mediatype')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    media_type_enum = postgresql.ENUM(name='mediatype')
    media_type_enum.drop(op.get_bind())

    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.alter_column('type_media',
               existing_type=sa.Enum('IMAGE', 'VIDEO', 'AUDIO', name='mediatype'),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
