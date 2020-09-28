from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('password', VARCHAR(length=10)),
    Column('email', VARCHAR(length=50)),
    Column('registered_on', TIMESTAMP),
    Column('is_super_user', BOOLEAN),
    Column('username', VARCHAR(length=20)),
    Column('logo_name', VARCHAR(length=200)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=20)),
    Column('password', String(length=10)),
    Column('email', String(length=50)),
    Column('registered_on', DateTime),
    Column('is_super_user', Boolean),
    Column('school_logo_name', String(length=200)),
    Column('matya_logo_name', String(length=200)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['logo_name'].drop()
    post_meta.tables['user'].columns['matya_logo_name'].create()
    post_meta.tables['user'].columns['school_logo_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['logo_name'].create()
    post_meta.tables['user'].columns['matya_logo_name'].drop()
    post_meta.tables['user'].columns['school_logo_name'].drop()
