from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from ..model import TableBase

class Tag(TableBase):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('tag.id'))
    name = Column(String)
    desc = Column(String)

    parent = relationship('Tag', remote_side=[id])
    children = relationship('Tag')

    def __init__(self, id=None, name=None, desc=None, parent=None, children=[]):
        self.id = id
        self.name = name
        self.desc = desc
        self.parent = parent
        self.children = children

    def __repr__(self):
        return "Tag(id=%s, name=%s, desc=%s, parent=%s, children=%s)" % (
                repr(self.id),
                repr(self.name),
                repr(self.desc),
                repr(self.parent),
                repr(self.children))
