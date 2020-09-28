from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_general_txt = Table('std_general_txt', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('general_txt_id', Integer, primary_key=True, nullable=False),
    Column('due_date', Date),
    Column('status_id', Integer),
    Column('acc_id', Integer),
    Column('scrt_id', Integer),
    Column('editable', Boolean),
    Column('selected', Boolean),
    Column('hide', Boolean),
)

std_resource = Table('std_resource', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('resource_id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=200)),
    Column('body', VARCHAR(length=500)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('dst_id', INTEGER),
    Column('goal_id', INTEGER),
    Column('who_id', INTEGER),
    Column('who_title', VARCHAR(length=140)),
    Column('status_id', INTEGER),
    Column('status_title', VARCHAR(length=200)),
    Column('status_color', VARCHAR(length=10)),
    Column('due_date', DATE),
)

std_resource = Table('std_resource', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('resource_id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=200)),
    Column('body', String(length=500)),
    Column('selected', Boolean),
    Column('hide', Boolean),
    Column('gt_id', Integer),
    Column('goal_id', Integer),
    Column('who_id', Integer),
    Column('who_title', String(length=140)),
    Column('status_id', Integer),
    Column('status_title', String(length=200)),
    Column('status_color', String(length=10)),
    Column('due_date', Date),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_general_txt'].columns['editable'].create()
    pre_meta.tables['std_resource'].columns['dst_id'].drop()
    post_meta.tables['std_resource'].columns['gt_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_general_txt'].columns['editable'].drop()
    pre_meta.tables['std_resource'].columns['dst_id'].create()
    post_meta.tables['std_resource'].columns['gt_id'].drop()
