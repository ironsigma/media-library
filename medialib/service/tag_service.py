from ..model import Tag

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
