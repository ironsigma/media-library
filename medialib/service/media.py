from .. model import Media
from ..model import Rating

class MediaService:
    def __init__(self, session):
        self.session = session

    def find(self, parent=None, rating=None):
        g_rating = self.session.query(Rating).filter_by(name='G')
        return self.session.query(Media) \
                .order_by(Media.title) \
                .filter(Media.cover != None) \
                .filter(Media.rating != None) \
                .filter(Media.parent == parent) \
                .filter(Media.rating.has(name='G'))
