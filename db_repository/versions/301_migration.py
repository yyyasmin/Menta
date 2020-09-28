from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
general_txt = Table('general_txt', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('author_id', INTEGER),
    Column('txt_type_id', INTEGER),
    Column('type', VARCHAR(length=50)),
    Column('title', VARCHAR(length=255), nullable=False),
    Column('body', VARCHAR(length=400)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt'].columns['txt_type_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt'].columns['txt_type_id'].create()
