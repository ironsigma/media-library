"""The database model used to store media"""

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base

TableBase = declarative_base()

_media_tag = Table('media_tag', TableBase.metadata,
        Column('media_id', Integer, ForeignKey('media.id')),
        Column('tag_id', Integer, ForeignKey('tag.id'))
)

_media_subrating = Table('media_subrating', TableBase.metadata,
        Column('media_id', Integer, ForeignKey('media.id')),
        Column('subrating_id', Integer, ForeignKey('subrating.id'))
)

from .media import Media
from .media import Rating
from .media import Subrating
from .tag import Tag

del media
del tag
