from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_document = Table('std_document', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('document_id', INTEGER, primary_key=True, nullable=False),
    Column('dst_id', INTEGER),
    Column('goal_id', INTEGER),
    Column('who_id', INTEGER),
    Column('who_title', VARCHAR(length=140)),
    Column('status_id', INTEGER),
    Column('status_title', VARCHAR(length=200)),
    Column('status_color', VARCHAR(length=10)),
    Column('due_date', DATE),
    Column('title', VARCHAR(length=200)),
    Column('body', VARCHAR(length=500)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_document'].columns['dst_id'].drop()
    pre_meta.tables['std_document'].columns['due_date'].drop()
    pre_meta.tables['std_document'].columns['goal_id'].drop()
    pre_meta.tables['std_document'].columns['status_color'].drop()
    pre_meta.tables['std_document'].columns['status_id'].drop()
    pre_meta.tables['std_document'].columns['status_title'].drop()
    pre_meta.tables['std_document'].columns['who_id'].drop()
    pre_meta.tables['std_document'].columns['who_title'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_document'].columns['dst_id'].create()
    pre_meta.tables['std_document'].columns['due_date'].create()
    pre_meta.tables['std_document'].columns['goal_id'].create()
    pre_meta.tables['std_document'].columns['status_color'].create()
    pre_meta.tables['std_document'].columns['status_id'].create()
    pre_meta.tables['std_document'].columns['status_title'].create()
    pre_meta.tables['std_document'].columns['who_id'].create()
    pre_meta.tables['std_document'].columns['who_title'].create()
