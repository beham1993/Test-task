from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', Text),
    Column('like', Integer),
    Column('author_id', Integer),
    Column('question_id', Integer),
)

question = Table('question', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String),
    Column('user_id', Integer),
)

question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=140)),
    Column('author_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].columns['author_id'].create()
    post_meta.tables['answer'].columns['question_id'].create()
    pre_meta.tables['question'].columns['user_id'].drop()
    post_meta.tables['question'].columns['author_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].columns['author_id'].drop()
    post_meta.tables['answer'].columns['question_id'].drop()
    pre_meta.tables['question'].columns['user_id'].create()
    post_meta.tables['question'].columns['author_id'].drop()
