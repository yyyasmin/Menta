from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
due_date = Table('due_date', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('goal_id', Integer, primary_key=True, nullable=False),
    Column('dst_id', Integer),
    Column('title', String(length=140)),
    Column('selected', Boolean),
    Column('due_date', DateTime),
    Column('status', String(length=100), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['due_date'].columns['dst_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['due_date'].columns['dst_id'].drop()
