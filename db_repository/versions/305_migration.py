from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
document_ufile_relationships = Table('document_ufile_relationships', pre_meta,
    Column('document_id', INTEGER),
    Column('ufile_id', INTEGER),
)

general_choice = Table('general_choice', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('author_id', INTEGER),
    Column('title', VARCHAR(length=255)),
    Column('body', VARCHAR(length=400)),
    Column('type', VARCHAR(length=50)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

general_txt_general_choice = Table('general_txt_general_choice', pre_meta,
    Column('general_txt_id', INTEGER, primary_key=True, nullable=False),
    Column('general_choice_id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=140)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

general_txt_resource_relationships = Table('general_txt_resource_relationships', pre_meta,
    Column('general_txt_id', INTEGER),
    Column('resource_id', INTEGER),
)

resource_general_choice = Table('resource_general_choice', pre_meta,
    Column('general_choice_id', INTEGER, primary_key=True, nullable=False),
    Column('resource_id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=140)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
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

std_general_choice = Table('std_general_choice', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('general_choice_id', INTEGER, primary_key=True, nullable=False),
    Column('due_date', DATE),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

txt_type = Table('txt_type', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=255)),
    Column('body', VARCHAR(length=400)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

general_txt = Table('general_txt', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author_id', Integer),
    Column('type', String(length=50)),
    Column('title', String(length=255), nullable=False),
    Column('body', String(length=400)),
    Column('due_date', Date),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['document_ufile_relationships'].drop()
    pre_meta.tables['general_choice'].drop()
    pre_meta.tables['general_txt_general_choice'].drop()
    pre_meta.tables['general_txt_resource_relationships'].drop()
    pre_meta.tables['resource_general_choice'].drop()
    pre_meta.tables['std_document'].drop()
    pre_meta.tables['std_document_relationships'].drop()
    pre_meta.tables['std_general_choice'].drop()
    pre_meta.tables['txt_type'].drop()
    post_meta.tables['general_txt'].columns['due_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['document_ufile_relationships'].create()
    pre_meta.tables['general_choice'].create()
    pre_meta.tables['general_txt_general_choice'].create()
    pre_meta.tables['general_txt_resource_relationships'].create()
    pre_meta.tables['resource_general_choice'].create()
    pre_meta.tables['std_document'].create()
    pre_meta.tables['std_document_relationships'].create()
    pre_meta.tables['std_general_choice'].create()
    pre_meta.tables['txt_type'].create()
    post_meta.tables['general_txt'].columns['due_date'].drop()
