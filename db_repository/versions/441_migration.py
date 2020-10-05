from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
star = Table('star', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('hide', BOOLEAN),
    Column('selected', BOOLEAN),
    Column('text', VARCHAR(length=50)),
    Column('idx_letter', VARCHAR(length=1)),
)

teacher = Table('teacher', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('first_name', String(length=20)),
    Column('last_name', String(length=20)),
    Column('birth_date', DateTime, nullable=False),
    Column('email', String(length=50)),
    Column('author_id', Integer),
    Column('registered_on', Date),
    Column('profetional', String(length=140)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)

school = Table('school', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('school_logo_name', String(length=200)),
    Column('matya_logo_name', String(length=200)),
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
    pre_meta.tables['star'].drop()
    post_meta.tables['teacher'].columns['user_id'].create()
    post_meta.tables['school'].columns['matya_logo_name'].create()
    post_meta.tables['school'].columns['school_logo_name'].create()
    post_meta.tables['user'].columns['is_super_user'].create()
    post_meta.tables['user'].columns['matya_logo_name'].create()
    post_meta.tables['user'].columns['school_logo_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['star'].create()
    post_meta.tables['teacher'].columns['user_id'].drop()
    post_meta.tables['school'].columns['matya_logo_name'].drop()
    post_meta.tables['school'].columns['school_logo_name'].drop()
    post_meta.tables['user'].columns['is_super_user'].drop()
    post_meta.tables['user'].columns['matya_logo_name'].drop()
    post_meta.tables['user'].columns['school_logo_name'].drop()
