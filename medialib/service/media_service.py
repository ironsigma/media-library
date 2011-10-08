from ..model import Media
from storm.expr import And

class MediaService:
    store = None

    def __init__(self, store):
        self.store = store

    def get_by_id(self, id):
        return self.store.get(Media, id)

    def find(self, parent=None, rating=None):
        if rating is None:
            return self.store.find(Media, And(Media.parent == parent, Media.type == Media.MOVIE))
        return self.store.find(Media, And(Media.rated == rating, And(Media.parent == parent, Media.type == Media.MOVIE)))
