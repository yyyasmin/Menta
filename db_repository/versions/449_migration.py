from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
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
    pre_meta.tables['star'].columns['text'].drop()
    post_meta.tables['star'].columns['body'].create()
    post_meta.tables['star'].columns['title'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['star'].columns['text'].create()
    post_meta.tables['star'].columns['body'].drop()
    post_meta.tables['star'].columns['title'].drop()
