from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
general_txt_resource = Table('general_txt_resource', pre_meta,
    Column('general_txt_id', INTEGER, primary_key=True, nullable=False),
    Column('resource_id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=140)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

resource_ufile_relationships = Table('resource_ufile_relationships', pre_meta,
    Column('resource_id', INTEGER),
    Column('ufile_id', INTEGER),
)

std_resource = Table('std_resource', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('resource_id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=200)),
    Column('body', VARCHAR(length=500)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('gt_id', INTEGER),
    Column('goal_id', INTEGER),
    Column('who_id', INTEGER),
    Column('who_title', VARCHAR(length=140)),
    Column('status_id', INTEGER),
    Column('status_title', VARCHAR(length=200)),
    Column('status_color', VARCHAR(length=10)),
    Column('due_date', DATE),
)

ufile_general_txt = Table('ufile_general_txt', post_meta,
    Column('ufile_id', Integer, primary_key=True, nullable=False),
    Column('general_txt_id', Integer, primary_key=True, nullable=False),
    Column('selected', Boolean),
    Column('hide', Boolean),
)

resource = Table('resource', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('type', VARCHAR(length=50)),
    Column('author_id', INTEGER),
    Column('title', VARCHAR(length=140)),
    Column('body', VARCHAR(length=255)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt_resource'].drop()
    pre_meta.tables['resource_ufile_relationships'].drop()
    pre_meta.tables['std_resource'].drop()
    post_meta.tables['ufile_general_txt'].create()
    pre_meta.tables['resource'].columns['author_id'].drop()
    pre_meta.tables['resource'].columns['body'].drop()
    pre_meta.tables['resource'].columns['hide'].drop()
    pre_meta.tables['resource'].columns['selected'].drop()
    pre_meta.tables['resource'].columns['title'].drop()
    pre_meta.tables['resource'].columns['type'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt_resource'].create()
    pre_meta.tables['resource_ufile_relationships'].create()
    pre_meta.tables['std_resource'].create()
    post_meta.tables['ufile_general_txt'].drop()
    pre_meta.tables['resource'].columns['author_id'].create()
    pre_meta.tables['resource'].columns['body'].create()
    pre_meta.tables['resource'].columns['hide'].create()
    pre_meta.tables['resource'].columns['selected'].create()
    pre_meta.tables['resource'].columns['title'].create()
    pre_meta.tables['resource'].columns['type'].create()
