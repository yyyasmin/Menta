from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
document = Table('document', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=140)),
    Column('body', VARCHAR(length=255)),
    Column('selected', BOOLEAN),
)

document_ufile_relationships = Table('document_ufile_relationships', pre_meta,
    Column('document_id', INTEGER),
    Column('ufile_id', INTEGER),
)

general_txt_resource_relationships = Table('general_txt_resource_relationships', pre_meta,
    Column('general_txt_id', INTEGER),
    Column('resource_id', INTEGER),
)

std_document = Table('std_document', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('document_id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=200)),
    Column('body', VARCHAR(length=500)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

std_document_relationships = Table('std_document_relationships', pre_meta,
    Column('student_id', INTEGER),
    Column('document_id', INTEGER),
)

documents = Table('documents', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

general_txt_resource = Table('general_txt_resource', post_meta,
    Column('general_txt_id', Integer, primary_key=True, nullable=False),
    Column('resource_id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)

resource_general_choice = Table('resource_general_choice', post_meta,
    Column('general_choice_id', Integer, primary_key=True, nullable=False),
    Column('resource_id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)

resource = Table('resource', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('type', String(length=50)),
    Column('title', String(length=140)),
    Column('body', String(length=255)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['document'].drop()
    pre_meta.tables['document_ufile_relationships'].drop()
    pre_meta.tables['general_txt_resource_relationships'].drop()
    pre_meta.tables['std_document'].drop()
    pre_meta.tables['std_document_relationships'].drop()
    post_meta.tables['documents'].create()
    post_meta.tables['general_txt_resource'].create()
    post_meta.tables['resource_general_choice'].create()
    post_meta.tables['resource'].columns['hide'].create()
    post_meta.tables['resource'].columns['type'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['document'].create()
    pre_meta.tables['document_ufile_relationships'].create()
    pre_meta.tables['general_txt_resource_relationships'].create()
    pre_meta.tables['std_document'].create()
    pre_meta.tables['std_document_relationships'].create()
    post_meta.tables['documents'].drop()
    post_meta.tables['general_txt_resource'].drop()
    post_meta.tables['resource_general_choice'].drop()
    post_meta.tables['resource'].columns['hide'].drop()
    post_meta.tables['resource'].columns['type'].drop()
