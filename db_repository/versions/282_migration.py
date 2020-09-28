from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_background = Table('std_background', pre_meta,
    Column('student_id', INTEGER, primary_key=True, nullable=False),
    Column('background_title', VARCHAR(length=300)),
    Column('background_body', TEXT),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

student = Table('student', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=20)),
    Column('last_name', String(length=20)),
    Column('birth_date', Date, nullable=False),
    Column('grade', String(length=10)),
    Column('background', String),
    Column('registered_on', Date),
    Column('selected', Boolean),
    Column('hide', Boolean),
    Column('profile_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_background'].drop()
    post_meta.tables['student'].columns['background'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_background'].create()
    post_meta.tables['student'].columns['background'].drop()
