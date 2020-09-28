from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
destination = Table('destination', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('author_id', INTEGER),
    Column('title', VARCHAR(length=255), nullable=False),
    Column('body', VARCHAR(length=400)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('age_range_id', INTEGER),
    Column('scrt_id', INTEGER),
    Column('goal_id', INTEGER),
)

goal = Table('goal', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author_id', Integer),
    Column('title', String(length=140)),
    Column('body', String(length=400)),
    Column('selected', Boolean),
    Column('dst_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['destination'].columns['goal_id'].drop()
    post_meta.tables['goal'].columns['dst_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['destination'].columns['goal_id'].create()
    post_meta.tables['goal'].columns['dst_id'].drop()
