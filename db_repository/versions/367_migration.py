from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ufile_general_txt = Table('ufile_general_txt', pre_meta,
    Column('ufile_id', INTEGER, primary_key=True, nullable=False),
    Column('general_txt_id', INTEGER, primary_key=True, nullable=False),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
)

general_txt = Table('general_txt', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author_id', Integer),
    Column('ufile_id', Integer),
    Column('type', String(length=50)),
    Column('h_name', String(length=50)),
    Column('e_name', String(length=50)),
    Column('gt_type', String(length=50)),
    Column('class_name', String(length=50)),
    Column('title', String(length=255), nullable=False),
    Column('body', String(length=400)),
    Column('default', Boolean),
    Column('color_txt', String(length=10)),
    Column('color', String(length=10)),
    Column('selected', Boolean),
    Column('hide', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['ufile_general_txt'].drop()
    post_meta.tables['general_txt'].columns['ufile_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['ufile_general_txt'].create()
    post_meta.tables['general_txt'].columns['ufile_id'].drop()
