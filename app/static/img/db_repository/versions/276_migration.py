from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_destination = Table('std_destination', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('destination_id', Integer, primary_key=True, nullable=False),
    Column('tag_id', Integer),
    Column('destination_title', String(length=300)),
    Column('destination_body', String(length=500)),
    Column('status_id', Integer),
    Column('status_title', String(length=200)),
    Column('status_color', String(length=10)),
    Column('due_date', Date),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_destination'].columns['tag_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_destination'].columns['tag_id'].drop()
