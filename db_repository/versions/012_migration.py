from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer = Table('answer', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String),
    Column('like', Integer),
    Column('author_id', Integer),
    Column('question', Integer),
)

answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', Text),
    Column('like', Integer),
    Column('user_id', Integer),
    Column('question_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answer'].columns['author_id'].drop()
    pre_meta.tables['answer'].columns['question'].drop()
    post_meta.tables['answer'].columns['question_id'].create()
    post_meta.tables['answer'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['answer'].columns['author_id'].create()
    pre_meta.tables['answer'].columns['question'].create()
    post_meta.tables['answer'].columns['question_id'].drop()
    post_meta.tables['answer'].columns['user_id'].drop()
