from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
todo = Table('todo', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=400)),
    Column('body', String(length=500)),
    Column('who_id', Integer),
    Column('who_title', String(length=140)),
    Column('status_id', Integer),
    Column('status_title', String(length=300)),
    Column('status_color', String(length=10)),
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
    post_meta.tables['todo'].columns['status_color'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['todo'].columns['status_color'].drop()
