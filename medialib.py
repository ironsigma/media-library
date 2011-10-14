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
    THUMB_WIDTH = 143
    THUMB_HEIGHT = 200

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setGeometry(100, 50, 1400, 800)
        self.setWindowTitle('Media Library')

        Cover.COVER_PATH = '/data/Media/Movies/Children/Covers/'
        self.cover_list = []

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

        # movies
        for media in media_service.find():
            cover = Cover(self, media, MediaLibrary.THUMB_WIDTH, MediaLibrary.THUMB_HEIGHT)
            cover.clicked.connect(self._start_movie)
            self.cover_list.append(cover)

        # build grid
        columns = self.width() // (MediaLibrary.THUMB_WIDTH + 10)
        for (cover, row, col) in self._get_grid_pos(self.cover_list, columns):
            self.grid.addWidget(cover, row, col)

        # add scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidget(pane)

        vbox = QVBoxLayout()
        vbox.addWidget(scrollArea)
        self.setLayout(vbox)

    def _start_movie(self):
        media = self.sender().media
        subprocess.Popen(['/usr/bin/totem', '--replace', MediaLibrary.MOVIES + media.file])

    def _get_grid_pos(self, items, columns):
        pos = []
        row = 0
        col = 0
        for item in items:
            if col >= columns:
                col = 0
                row += 1
            pos.append((item, row, col))
            col += 1
        return pos

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = MediaLibrary()
    panel.show()
    sys.exit(app.exec_())
    app.quit()
