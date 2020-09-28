from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_general_txt = Table('std_general_txt', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('general_txt_id', INTEGER, primary_key=True, nullable=False),
    Column('due_date', DATE),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('status_id', INTEGER),
    Column('acc_id', INTEGER),
    Column('scrt_id', INTEGER),
    Column('editable', BOOLEAN),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_general_txt'].columns['editable'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_general_txt'].columns['editable'].create()
