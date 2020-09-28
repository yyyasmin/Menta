from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dst_goal_relationships = Table('dst_goal_relationships', pre_meta,
    Column('destination_id', INTEGER),
    Column('goal_id', INTEGER),
)

destination = Table('destination', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author_id', Integer),
    Column('title', String(length=255), nullable=False),
    Column('body', String(length=400)),
    Column('selected', Boolean),
    Column('hide', Boolean),
    Column('age_range_id', Integer),
    Column('scrt_id', Integer),
    Column('goal_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dst_goal_relationships'].drop()
    post_meta.tables['destination'].columns['goal_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dst_goal_relationships'].create()
    post_meta.tables['destination'].columns['goal_id'].drop()
