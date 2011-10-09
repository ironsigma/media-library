#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from medialib.service import MediaService
from medialib.model import Media
import math
#import subprocess

class MediaLibrary:
    COVERS = '/data/Media/Movies/Children/Covers/'
    MOVIES = '/data/Media/Movies/Children/'
    COLS = 7
    WINDOW_HEIGHT = 650

    ASPECT_RATIO = 1.4
    THUMB_WIDTH = 142
    THUMB_SPACING = 16

    def __init__(self):
        self.THUMB_HEIGHT = self.THUMB_WIDTH * self.ASPECT_RATIO

        # fetch media
        engine = create_engine('sqlite:///medialib.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        media_service = MediaService(session)

        # movie table
        media_list = media_service.find()
        rows = int(math.ceil(media_list.count() / float(self.COLS)))
        print("table: %dx%d" % (rows, self.COLS))
        row = 0
        col = 0
        for media in media_list:
            if row >= self.COLS:
                row = 0
                col += 1
            self._add_movie(row, col, media)
            row += 1

    def _start_movie(self, widget, data=None):
        print("totem --replace %s" % (data))
        #subprocess.Popen(['/usr/bin/totem', '--replace', data])

    def _add_movie(self, row, col, media):
        if media.cover is None:
            cover = 'no_cover.jpg'
        else:
            cover = media.cover

        #print("cover: (%dx%d) %s%s" % (self.THUMB_WIDTH, self.THUMB_HEIGHT, self.COVERS, cover))
        #print("added at: %d, %d" % (row, col))
        #print('file: %s%s' % (self.MOVIES, media.file))

if __name__ == '__main__':
    MediaLibrary()
