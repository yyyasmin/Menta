from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_general_txt = Table('std_general_txt', post_meta,
    Column('student_id', Integer, primary_key=True, nullable=False),
    Column('general_txt_id', Integer, primary_key=True, nullable=False),
    Column('due_date', Date),
    Column('status_id', Integer),
    Column('acc_id', Integer),
    Column('scrt_id', Integer),
    Column('selected', Boolean),
    Column('hide', Boolean),
)

general_txt = Table('general_txt', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('author_id', INTEGER),
    Column('type', VARCHAR(length=50)),
    Column('title', VARCHAR(length=255), nullable=False),
    Column('body', VARCHAR(length=400)),
    Column('due_date', DATE),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_general_txt'].columns['scrt_id'].create()
    pre_meta.tables['general_txt'].columns['due_date'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_general_txt'].columns['scrt_id'].drop()
    pre_meta.tables['general_txt'].columns['due_date'].create()
