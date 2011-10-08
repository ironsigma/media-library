from storm.locals import Int, Unicode, Reference, ReferenceSet

class Tag(object):
    __storm_table__ = 'tag'

    id = Int(primary=True)
    parent_id = Int()
    name = Unicode()
    description = Unicode(name='desc')

    parent = Reference(parent_id, id)
    children = ReferenceSet(id, parent_id)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "id: %s, parent: %s, name: %s, description: %s" % (
                self.id, self.parent_id, self.name, self.description)

class MediaTag(object):
    __storm_table__ = 'media_tag'
    __storm_primary__ = 'media_id', 'tag_id'
    media_id = Int()
    tag_id = Int()

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

def create_schema(store, file):
    store.execute('''CREATE TABLE media (
            id INTEGER PRIMARY KEY,
            parent_id INTEGER,
            type INTEGER,
            file TEXT,
            cover TEXT,
            title TEXT,
            release INTEGER,
            rated TEXT,
            desc TEXT)''')

    store.execute('''CREATE TABLE media_tag (
            media_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (media_id, tag_id))''')

    store.execute('''CREATE TABLE tag (
            id INTEGER PRIMARY KEY,
            parent_id INTEGER,
            name TEXT,
            desc TEXT)''')

if __name__ == "__main__":
    from storm.locals import Store, create_database
    import sys

    if len(sys.argv) == 1:
        print "Creates the sqlite3 database."
        print "\tusage: <file>"
        sys.exit(1)

    db = create_database('sqlite:///' + sys.argv[1])
    store = Store(db)
    create_schema(store, sys.argv[1])
    store.commit()
