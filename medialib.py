import sys
import math
import subprocess

# UI
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from medialib.ui import Cover

# SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from medialib.service import MediaService
from medialib.model import Media

class MediaLibrary(QWidget):
    MOVIES = '/data/Media/Movies/Children/'
    COLS = 7
    THUMB_WIDTH = 143
    THUMB_HEIGHT = 200 # THUMB_WIDTH * ASPECT_RATIO(1.4)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        Cover.COVER_PATH = '/data/Media/Movies/Children/Covers/'

        #ui
        self.grid = QGridLayout()

        pane = QWidget()
        pane.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pane.setLayout(self.grid)

        # fetch media
        engine = create_engine('sqlite:///medialib.db', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        media_service = MediaService(session)

        # movie table
        media_list = media_service.find()
        rows = int(math.ceil(media_list.count() / float(MediaLibrary.COLS)))
        row = 0
        col = 0
        for media in media_list:
            if col >= MediaLibrary.COLS:
                col = 0
                row += 1
            self._add_movie(row, col, media)
            col += 1

        # add scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidget(pane)

        vbox = QVBoxLayout()
        vbox.addWidget(scrollArea)
        self.setLayout(vbox)

    def _start_movie(self):
        media = self.sender().media
        subprocess.Popen(['/usr/bin/totem', '--replace', MediaLibrary.MOVIES + media.file])

    def _add_movie(self, row, col, media):
        cover = Cover(self, media, MediaLibrary.THUMB_WIDTH, MediaLibrary.THUMB_HEIGHT)
        self.grid.addWidget(cover, row, col)
        cover.clicked.connect(self._start_movie)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = MediaLibrary()
    panel.show()
    sys.exit(app.exec_())
    app.quit()
