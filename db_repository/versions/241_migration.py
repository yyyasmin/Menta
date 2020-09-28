from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
todo = Table('todo', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=400)),
    Column('body', VARCHAR(length=500)),
    Column('who_id', INTEGER),
    Column('who_title', VARCHAR(length=140)),
    Column('status_id', INTEGER),
    Column('status_title', VARCHAR(length=300)),
    Column('status_color', VARCHAR(length=10)),
    Column('due_date', DATE),
    Column('goal_id', INTEGER),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

std_goal = Table('std_goal', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('goal_id', Integer, primary_key=True, nullable=False),
    Column('dst_id', Integer),
    Column('status_id', Integer),
    Column('due_date', Date),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['todo'].columns['due_date'].drop()
    post_meta.tables['std_goal'].columns['due_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['todo'].columns['due_date'].create()
    post_meta.tables['std_goal'].columns['due_date'].drop()
