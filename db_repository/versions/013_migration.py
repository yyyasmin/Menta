from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
std_general_txt_relationships = Table('std_general_txt_relationships', pre_meta,
    Column('student_id', INTEGER),
    Column('general_txt_id', INTEGER),
)

menta_db = Table('menta_db', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

strength = Table('strength', pre_meta,
    Column('general_txt_id', INTEGER, primary_key=True, nullable=False),
)

strength = Table('strength', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

student = Table('student', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('first_name', VARCHAR(length=20)),
    Column('last_name', VARCHAR(length=20)),
    Column('birth_date', DATE, nullable=False),
    Column('grade', VARCHAR(length=10)),
    Column('background', VARCHAR),
    Column('registered_on', DATE),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('profile_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_general_txt_relationships'].drop()
    post_meta.tables['menta_db'].create()
    pre_meta.tables['strength'].columns['general_txt_id'].drop()
    post_meta.tables['strength'].columns['id'].create()
    pre_meta.tables['student'].columns['profile_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['std_general_txt_relationships'].create()
    post_meta.tables['menta_db'].drop()
    pre_meta.tables['strength'].columns['general_txt_id'].create()
    post_meta.tables['strength'].columns['id'].drop()
    pre_meta.tables['student'].columns['profile_id'].create()
