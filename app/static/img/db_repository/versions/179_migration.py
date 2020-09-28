from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
stength_relationships = Table('stength_relationships', pre_meta,
    Column('profile_id', INTEGER),
    Column('strength_id', INTEGER),
)

profile_strength_relationships = Table('profile_strength_relationships', post_meta,
    Column('profile_id', Integer),
    Column('strength_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['stength_relationships'].drop()
    post_meta.tables['profile_strength_relationships'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['stength_relationships'].create()
    post_meta.tables['profile_strength_relationships'].drop()
