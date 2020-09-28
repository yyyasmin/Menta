from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_todo = Table('std_todo', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('todo_id', INTEGER, primary_key=True, nullable=False),
    Column('dst_id', INTEGER),
    Column('goal_id', INTEGER),
    Column('who_id', INTEGER),
    Column('who_title', VARCHAR(length=140)),
    Column('status_id', INTEGER),
    Column('status_title', VARCHAR(length=200)),
    Column('status_color', VARCHAR(length=10)),
    Column('due_date', DATE),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('todo_body', INTEGER),
    Column('todo_title', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_todo'].columns['todo_body'].drop()
    pre_meta.tables['std_todo'].columns['todo_title'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_todo'].columns['todo_body'].create()
    pre_meta.tables['std_todo'].columns['todo_title'].create()
