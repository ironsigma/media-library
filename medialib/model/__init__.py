"""The database model used to store media"""

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base

TableBase = declarative_base()

_media_tag = Table('media_tag', TableBase.metadata,
        Column('media_id', Integer, ForeignKey('media.id')),
        Column('tag_id', Integer, ForeignKey('tag.id'))
)

from .media import Media
from .tag import Tag

del media
del tag
