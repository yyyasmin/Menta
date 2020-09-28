from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dst_tag_relationships = Table('dst_tag_relationships', pre_meta,
    Column('tag_id', INTEGER),
    Column('destination_id', INTEGER),
)

dst__tag = Table('dst__tag', post_meta,
    Column('destination_id', Integer, primary_key=True, nullable=False),
    Column('tag_id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('selected', Boolean),
    Column('status', String(length=100), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dst_tag_relationships'].drop()
    post_meta.tables['dst__tag'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dst_tag_relationships'].create()
    post_meta.tables['dst__tag'].drop()
