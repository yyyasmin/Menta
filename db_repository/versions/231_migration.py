from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
due_date = Table('due_date', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('goal_id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=140)),
    Column('selected', BOOLEAN),
    Column('due_date', TIMESTAMP),
    Column('status', VARCHAR(length=100), nullable=False),
    Column('dst_id', INTEGER),
)

std_goal = Table('std_goal', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('goal_id', Integer, primary_key=True, nullable=False),
    Column('dst_id', Integer, primary_key=True, nullable=False),
    Column('status_id', Integer),
    Column('title', String(length=140)),
    Column('body', String(length=500)),
    Column('selected', Boolean),
    Column('due_date', DateTime),
)

std_todo = Table('std_todo', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('todo_id', Integer, primary_key=True, nullable=False),
    Column('dst_id', Integer, primary_key=True, nullable=False),
    Column('status_id', Integer),
    Column('title', String(length=140)),
    Column('body', String(length=500)),
    Column('due_date', DateTime),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['due_date'].drop()
    post_meta.tables['std_goal'].create()
    post_meta.tables['std_todo'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['due_date'].create()
    post_meta.tables['std_goal'].drop()
    post_meta.tables['std_todo'].drop()
