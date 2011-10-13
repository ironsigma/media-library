from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref, validates
from ..model import TableBase, _media_tag, _media_subrating

class Rating(TableBase):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)

    def __init__(self, id=None, name=None, desc=None):
        self.id = id
        self.name = name
        self.desc = desc

    def __repr__(self):
        return "Rating(id=%s, name=%s, desc=%s)" % (repr(self.id), repr(self.name), repr(self.desc))

class Subrating(TableBase):
    __tablename__ = 'subrating'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)

    def __init__(self, id=None, name=None, desc=None):
        self.id = id
        self.name = name
        self.desc = desc

    def __repr__(self):
        return "Subrating(id=%s, name=%s, desc=%s)" % (repr(self.id), repr(self.name), repr(self.desc))

class Media(TableBase):
    __tablename__ = 'media'

    _valid_types = frozenset(['Folder', 'Movie', 'Show'])

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    file = Column(String)
    cover = Column(String)
    release = Column(Integer)
    desc = Column(String)
    _rating_id = Column('rating_id', ForeignKey('rating.id'))
    _subrating_id = Column('subrating_id', ForeignKey('subrating.id'))
    _parent_id = Column('parent_id', ForeignKey('media.id'))

    rating = relationship('Rating')
    subratings = relationship('Subrating', secondary=_media_subrating, backref='media')
    parent = relationship('Media', remote_side=[id])
    children = relationship('Media')
    tags = relationship('Tag', secondary=_media_tag, backref='media')

    def __init__(self, id=None, title=None, type=None, file=None,
                 cover=None, release=None, desc=None, rating=None,
                 subratings=[], tags=[], parent=None, children=[]):

        self.id = id
        self.title = title
        self.type = type
        self.file = file
        self.cover = cover
        self.release = release
        self.desc = desc
        self.rating = rating
        self.subratings = subratings
        self.tags = tags
        self.parent = parent
        self.children = children

    @validates('type')
    def validate_type(self, key, value):
        if value is None:
            return value

        if value not in Media._valid_types:
            raise ValueError('Invalid media type "%s"' % value)
        return value

    def __repr__(self):
        return "Media(id=%s, title=%s, type=%s, file=%s, cover=%s, " \
               "release=%s, desc=%s, rating=%s, subratings=%s, " \
               "tags=%s, parent=%s, children=%s)" % (
                repr(self.id),
                repr(self.title),
                repr(self.type),
                repr(self.file),
                repr(self.cover),
                repr(self.release),
                repr(self.desc),
                repr(self.rating),
                repr(self.subratings),
                repr(self.tags),
                repr(self.parent),
                repr(self.children))
