from model import Media, Tag

class TagService:
    store = None

    def __init__(self, store):
        self.store = store

    def find_any_by_name(self, name):
        rs = self.store.find(Tag, Tag.name == name)
        if not rs.is_empty():
            return rs.any()
        return None

    def find_by_parent(self, parent=None):
        return self.store.find(Tag, Tag.parent == parent)

class MediaService:
    store = None

    def __init__(self, store):
        self.store = store

    def get_by_id(self, id):
        return self.store.get(Media, id)

    def find_by_parent(self, parent=None):
        return self.store.find(Media, Media.parent == parent)

if __name__ == '__main__':
    from storm.locals import Store, create_database
    db = create_database('sqlite:///media.db')
    store = Store(db)

    tag_service = TagService(store)
    media_service = MediaService(store)

    ratings = tag_service.find_any_by_name(u'__rating__')
    for rating in tag_service.find_by_parent(ratings):
        print rating

    #...dora = media_service.get_by_id(34)
    #...print dora

    #...for media in dora.children:
    #...    print media
    #...    print media.parent
    #...    break

    #...for media in media_service.find_by_parent():
    #...    print media
    #...    break
