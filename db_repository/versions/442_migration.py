from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menta_db = Table('menta_db', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

method = Table('method', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

method_type = Table('method_type', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

test = Table('test', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
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

star = Table('star', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('text', VARCHAR(length=50)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

star = Table('star', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=50)),
    Column('body', String(length=500)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menta_db'].create()
    post_meta.tables['method'].create()
    post_meta.tables['method_type'].create()
    post_meta.tables['test'].create()
    post_meta.tables['teacher'].columns['user_id'].create()
    post_meta.tables['school'].columns['matya_logo_name'].create()
    post_meta.tables['school'].columns['school_logo_name'].create()
    pre_meta.tables['star'].columns['text'].drop()
    post_meta.tables['star'].columns['body'].create()
    post_meta.tables['star'].columns['title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menta_db'].drop()
    post_meta.tables['method'].drop()
    post_meta.tables['method_type'].drop()
    post_meta.tables['test'].drop()
    post_meta.tables['teacher'].columns['user_id'].drop()
    post_meta.tables['school'].columns['matya_logo_name'].drop()
    post_meta.tables['school'].columns['school_logo_name'].drop()
    pre_meta.tables['star'].columns['text'].create()
    post_meta.tables['star'].columns['body'].drop()
    post_meta.tables['star'].columns['title'].drop()
