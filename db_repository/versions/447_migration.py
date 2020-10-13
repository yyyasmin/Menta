from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
method = Table('method', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

method_type = Table('method_type', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

test = Table('test', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['method'].create()
    post_meta.tables['method_type'].create()
    post_meta.tables['test'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['method'].drop()
    post_meta.tables['method_type'].drop()
    post_meta.tables['test'].drop()
