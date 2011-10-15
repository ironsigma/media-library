import sys
import math
import subprocess

# UI
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from medialib.ui import Cover
from medialib.ui import CoverTable

# SQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from medialib.service import MediaService
from medialib.model import Media

Cover.COVER_PATH = '/data/Media/Movies/Children/Covers/'

class MediaLibrary(QWidget):
    MOVIES = '/data/Media/Movies/Children/'
    THUMB_WIDTH = 143
    THUMB_HEIGHT = 200
    THUMB_SPACING = 7

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        # build table
        table = CoverTable(width=self.THUMB_WIDTH, height=self.THUMB_HEIGHT, spacing=self.THUMB_SPACING)
        for cover in self._fetch_covers():
            table.add(cover)

        # add scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidget(table)
        scrollArea.setWidgetResizable(True)

        # add scroll area to layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scrollArea)

        # add layout area to window
        self.setLayout(layout)
        self.resize(1375, 800)
        self.center()
        self.setWindowTitle('Media Library')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _fetch_covers(self):
        cover_list = []

        # connect to db
        engine = create_engine('sqlite:///medialib.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        media_service = MediaService(session)

        # fetch movies and create covers
        for media in media_service.find():
            cover = Cover(self, media, MediaLibrary.THUMB_WIDTH, MediaLibrary.THUMB_HEIGHT)
            cover.clicked.connect(self._start_movie)
            cover_list.append(cover)

        return cover_list

    def _start_movie(self):
        media = self.sender().media
        subprocess.Popen(['/usr/bin/totem', '--replace', MediaLibrary.MOVIES + media.file])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = MediaLibrary()
    panel.show()
    sys.exit(app.exec_())
    app.quit()
