from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
destination_relationships = Table('destination_relationships', pre_meta,
    Column('student_id', INTEGER),
    Column('destination_id', INTEGER),
)

profile_relationships = Table('profile_relationships', pre_meta,
    Column('student_id', INTEGER),
    Column('profile_id', INTEGER),
)

subject_relationships = Table('subject_relationships', pre_meta,
    Column('profile_id', INTEGER),
    Column('subject_id', INTEGER),
)

weakness_relationships = Table('weakness_relationships', pre_meta,
    Column('profile_id', INTEGER),
    Column('weakness_id', INTEGER),
)

profile_subject_relationships = Table('profile_subject_relationships', post_meta,
    Column('profile_id', Integer),
    Column('subject_id', Integer),
)

profile_weakness_relationships = Table('profile_weakness_relationships', post_meta,
    Column('profile_id', Integer),
    Column('weakness_id', Integer),
)

std_dst_relationships = Table('std_dst_relationships', post_meta,
    Column('student_id', Integer),
    Column('destination_id', Integer),
)

std_profile_relationships = Table('std_profile_relationships', post_meta,
    Column('student_id', Integer),
    Column('profile_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['destination_relationships'].drop()
    pre_meta.tables['profile_relationships'].drop()
    pre_meta.tables['subject_relationships'].drop()
    pre_meta.tables['weakness_relationships'].drop()
    post_meta.tables['profile_subject_relationships'].create()
    post_meta.tables['profile_weakness_relationships'].create()
    post_meta.tables['std_dst_relationships'].create()
    post_meta.tables['std_profile_relationships'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['destination_relationships'].create()
    pre_meta.tables['profile_relationships'].create()
    pre_meta.tables['subject_relationships'].create()
    pre_meta.tables['weakness_relationships'].create()
    post_meta.tables['profile_subject_relationships'].drop()
    post_meta.tables['profile_weakness_relationships'].drop()
    post_meta.tables['std_dst_relationships'].drop()
    post_meta.tables['std_profile_relationships'].drop()
