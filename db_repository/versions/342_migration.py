from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
general_txt = Table('general_txt', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('author_id', INTEGER),
    Column('type', VARCHAR(length=50)),
    Column('title', VARCHAR(length=255), nullable=False),
    Column('body', VARCHAR(length=400)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('gt_type_txt', VARCHAR(length=50)),
    Column('color', VARCHAR(length=10)),
    Column('color_txt', VARCHAR(length=10)),
)

general_txt = Table('general_txt', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author_id', Integer),
    Column('type', String(length=50)),
    Column('type_txt', String(length=50)),
    Column('title', String(length=255), nullable=False),
    Column('body', String(length=400)),
    Column('color_txt', String(length=10)),
    Column('color', String(length=10)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt'].columns['gt_type_txt'].drop()
    post_meta.tables['general_txt'].columns['type_txt'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt'].columns['gt_type_txt'].create()
    post_meta.tables['general_txt'].columns['type_txt'].drop()
