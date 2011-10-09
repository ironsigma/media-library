from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

media_tag = Table('media_tag', Base.metadata,
        Column('media_id', Integer, ForeignKey('media.id')),
        Column('tag_id', Integer, ForeignKey('tag.id'))
)

from .media import Media
from .tag import Tag

del media
del tag
