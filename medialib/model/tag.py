from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from ..model import TableBase

class Tag(TableBase):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('tag.id'))
    name = Column(String)
    description = Column('desc', String)

    parent = relationship('Tag', remote_side=[id])
    children = relationship('Tag')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag('%s', '%s','%s','%s')>" % (
                self.id,
                self.parent_id,
                self.name,
                self.description)
