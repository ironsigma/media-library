from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from ..model import TableBase, _media_tag

class Media(TableBase):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('media.id'))
    type = Column(String)
    file = Column(String)
    cover = Column(String)
    title = Column(String)
    release = Column(Integer)
    rated = Column(String)
    description = Column('desc', String)

    parent = relationship('Media', remote_side=[id])
    children = relationship('Media')
    tags = relationship('Tag', secondary=_media_tag, backref='media')

    def __init__(self, title, type):
        self.title = title
        self.type = type

    def __repr__(self):
        return "<Media('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
                self.id,
                self.parent_id,
                self.type,
                self.file,
                self.cover,
                self.title,
                self.release,
                self.rated,
                self.description)
