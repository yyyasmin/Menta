from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
general_txt = Table('general_txt', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author_id', Integer),
    Column('type', String(length=50)),
    Column('type_txt', String(length=50)),
    Column('title', String(length=255), nullable=False),
    Column('body', String(length=400)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['general_txt'].columns['type_txt'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['general_txt'].columns['type_txt'].drop()
