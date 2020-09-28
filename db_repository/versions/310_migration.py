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
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_general_txt'].columns['status_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['std_general_txt'].columns['status_id'].drop()
