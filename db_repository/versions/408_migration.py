from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
general_txt = Table('general_txt', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('author_id', INTEGER),
    Column('type', VARCHAR(length=50)),
    Column('h_name', VARCHAR(length=50)),
    Column('e_name', VARCHAR(length=50)),
    Column('gt_type', VARCHAR(length=50)),
    Column('class_name', VARCHAR(length=50)),
    Column('title', VARCHAR(length=255), nullable=False),
    Column('default', BOOLEAN),
    Column('selected', BOOLEAN),
    Column('hide', BOOLEAN),
    Column('ufile_id', INTEGER),
    Column('h_plural_name', VARCHAR(length=100)),
    Column('body', VARCHAR(length=500)),
    Column('color', VARCHAR(length=30)),
    Column('color_txt', VARCHAR(length=30)),
    Column('table_color', VARCHAR(length=30)),
    Column('title_color', VARCHAR(length=30)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt'].columns['color'].drop()
    pre_meta.tables['general_txt'].columns['color_txt'].drop()
    pre_meta.tables['general_txt'].columns['table_color'].drop()
    pre_meta.tables['general_txt'].columns['title_color'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['general_txt'].columns['color'].create()
    pre_meta.tables['general_txt'].columns['color_txt'].create()
    pre_meta.tables['general_txt'].columns['table_color'].create()
    pre_meta.tables['general_txt'].columns['title_color'].create()
