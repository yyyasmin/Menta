from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_document_relationships = Table('std_document_relationships', pre_meta,
    Column('student_id', INTEGER),
    Column('document_id', INTEGER),
)

document_ufile_relationships = Table('document_ufile_relationships', post_meta,
    Column('document_id', Integer),
    Column('ufile_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_document_relationships'].drop()
    post_meta.tables['document_ufile_relationships'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_document_relationships'].create()
    post_meta.tables['document_ufile_relationships'].drop()
