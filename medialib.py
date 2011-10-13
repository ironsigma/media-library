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
        MediaLibrary.THUMB_HEIGHT = MediaLibrary.THUMB_WIDTH * MediaLibrary.ASPECT_RATIO

        # fetch media
        engine = create_engine('sqlite:///medialib.db', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        media_service = MediaService(session)

        # movie table
        media_list = media_service.find()
        rows = int(math.ceil(media_list.count() / float(MediaLibrary.COLS)))
        print("table: %dx%d" % (rows, MediaLibrary.COLS))
        row = 0
        col = 0
        for media in media_list:
            if row >= MediaLibrary.COLS:
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

        print(media)

        if media.rating is not None:
            print(media.rating)

        if len(media.subratings) > 0:
            print(media.subratings)

        if len(media.tags) > 0:
            print(media.tags)

        #print("cover: (%dx%d) %s%s" % (MediaLibrary.THUMB_WIDTH, MediaLibrary.THUMB_HEIGHT, MediaLibrary.COVERS, cover))
        #print("added at: %d, %d" % (row, col))
        #print('file: %s%s' % (MediaLibrary.MOVIES, media.file))

if __name__ == '__main__':
    MediaLibrary()
