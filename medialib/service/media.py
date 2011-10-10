from ..model import Media

class MediaService:
    def __init__(self, session):
        self.session = session

    def find(self, parent=None, rating=None):
        return self.session.query(Media).filter_by(parent=parent)
