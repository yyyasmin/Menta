from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
todo = Table('todo', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=400)),
    Column('body', VARCHAR(length=500)),
    Column('who', INTEGER),
    Column('due_date', DATE),
    Column('goal_id', INTEGER),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('status', INTEGER),
)

todo = Table('todo', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=400)),
    Column('body', String(length=500)),
    Column('who_id', Integer),
    Column('status_id', Integer),
    Column('due_date', Date),
    Column('goal_id', Integer),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['todo'].columns['status'].drop()
    pre_meta.tables['todo'].columns['who'].drop()
    post_meta.tables['todo'].columns['status_id'].create()
    post_meta.tables['todo'].columns['who_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['todo'].columns['status'].create()
    pre_meta.tables['todo'].columns['who'].create()
    post_meta.tables['todo'].columns['status_id'].drop()
    post_meta.tables['todo'].columns['who_id'].drop()
