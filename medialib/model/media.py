from storm.locals import Int, Unicode, Reference, ReferenceSet
from media_tag import MediaTag
from tag import Tag

class Media(object):
    __storm_table__ = 'media'

    # constatns
    MOVIE   = 1
    TRAILER = 2
    SERIE   = 3
    SHOW    = 4
    CLIP    = 5

    # properties
    id = Int(primary=True)
    parent_id = Int()
    type = Int()
    file = Unicode()
    cover = Unicode()
    title = Unicode()
    release = Int()
    rated = Unicode()
    description = Unicode(name='desc')

    # references
    tags = ReferenceSet(id, MediaTag.media_id, MediaTag.tag_id, Tag.id)
    parent = Reference(parent_id, id)
    children = ReferenceSet(id, parent_id)

    def __init__(self, title, type):
        self.title = title
        self.type = type

    def __str__(self):
        return "id: %s, parent_id: %s, title: %s, type: %s, file: %s, cover: %s, release: %s, rated: %s,  description: %s" % (
                self.id, self.parent_id, self.title, self.type, self.file, self.cover, self.release, self.rated, self.description)
