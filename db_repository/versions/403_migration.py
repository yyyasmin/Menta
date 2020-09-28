from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    op.alter_column('General_txt', 'color_txt', existing_type=db.String(10), type_=db.String(30), nullable=True)
    op.alter_column('General_txt', 'color', existing_type=db.String(10), type_=db.String(30), nullable=True)
    op.alter_column('General_txt', 'table_color', existing_type=db.String(20), type_=db.String(30), nullable=True)
    op.alter_column('General_txt', 'title_color', existing_type=db.String(10), type_=db.String(30), nullable=True)



def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    op.alter_column('General_txt', 'color_txt', existing_type=db.String(30), type_=db.String(10), nullable=True)
    op.alter_column('General_txt', 'color', existing_type=db.String(30), type_=db.String(10), nullable=True)
    op.alter_column('General_txt', 'table_color', existing_type=db.String(30), type_=db.String(20), nullable=True)
    op.alter_column('General_txt', 'title_color', existing_type=db.String(30), type_=db.String(10), nullable=True)
