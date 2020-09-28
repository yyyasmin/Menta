from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
general_txt_general_choice = Table('general_txt_general_choice', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('general_txt_id', INTEGER, primary_key=True, nullable=False),
    Column('general_choice_id', INTEGER, primary_key=True, nullable=False),
    Column('title', VARCHAR(length=140)),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt_general_choice'].columns['id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt_general_choice'].columns['id'].create()
