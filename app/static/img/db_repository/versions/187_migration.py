from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dest_tag_relationships = Table('dest_tag_relationships', pre_meta,
    Column('destinatin_id', INTEGER),
    Column('tag_id', INTEGER),
)

dst_tag_relationships = Table('dst_tag_relationships', post_meta,
    Column('destinatin_id', Integer),
    Column('tag_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dest_tag_relationships'].drop()
    post_meta.tables['dst_tag_relationships'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['dest_tag_relationships'].create()
    post_meta.tables['dst_tag_relationships'].drop()
