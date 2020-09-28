from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
school = Table('school', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('logo_name', VARCHAR(length=200)),
)

school = Table('school', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('school_logo_name', String(length=200)),
    Column('matya_logo_name', String(length=200)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['school'].columns['logo_name'].drop()
    post_meta.tables['school'].columns['matya_logo_name'].create()
    post_meta.tables['school'].columns['school_logo_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['school'].columns['logo_name'].create()
    post_meta.tables['school'].columns['matya_logo_name'].drop()
    post_meta.tables['school'].columns['school_logo_name'].drop()
