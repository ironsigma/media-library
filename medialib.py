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

Cover.COVER_PATH = '/data/Media/Movies/Children/Covers/'

class MediaLibrary(QWidget):
    MOVIES = '/data/Media/Movies/Children/'
    THUMB_WIDTH = 143
    THUMB_HEIGHT = 200
    THUMB_SPACING = 8
    BORDER_WIDTH = 50

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

        # size and title
        self.setGeometry(100, 50, 1410, 800)
        self.setWindowTitle('Media Library')

        # grid and covers
        self.grid = QHBoxLayout()
        self.grid_column_list = []
        self.cover_list = []

        # pane
        self.pane = QWidget()
        self.pane.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pane.setLayout(self.grid)

        # connect to db
        engine = create_engine('sqlite:///medialib.db', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        media_service = MediaService(session)

        # fetch movies and create covers
        for media in media_service.find():
            cover = Cover(self, media, MediaLibrary.THUMB_WIDTH, MediaLibrary.THUMB_HEIGHT)
            cover.clicked.connect(self._start_movie)
            self.cover_list.append(cover)

        # build grid
        self._build_grid()

        # add scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.pane)

        # add scroll area to window
        vbox = QVBoxLayout()
        vbox.addWidget(scrollArea)
        self.setLayout(vbox)

    def resizeEvent(self, event):
        self._build_grid()

    def _start_movie(self):
        media = self.sender().media
        subprocess.Popen(['/usr/bin/totem', '--replace', MediaLibrary.MOVIES + media.file])

    def _build_grid(self):
        # num of columns
        num_columns = (self.width() - MediaLibrary.BORDER_WIDTH) // (MediaLibrary.THUMB_WIDTH + MediaLibrary.THUMB_SPACING)
        if num_columns <= 0: num_columns = 1

        # no change in num of columns
        if num_columns == len(self.grid_column_list):
            return

        # remove each column
        for grid_column in self.grid_column_list:
            self.grid.removeItem(grid_column)
            grid_column.deleteLater()

        # add new columns
        self.grid_column_list = []
        for i in range(num_columns):
            grid_column = QVBoxLayout()
            grid_column.setSpacing(MediaLibrary.THUMB_SPACING)
            self.grid_column_list.append(grid_column)
            self.grid.addLayout(grid_column)

        # add each item to column
        column_index = 0
        for cover in self.cover_list:
            if column_index >= num_columns:
                column_index = 0
            self.grid_column_list[column_index].addWidget(cover)
            column_index += 1

        # add padding to columns not full
        rows = math.ceil(len(self.cover_list) / float(num_columns))
        for grid_column in self.grid_column_list:
            if grid_column.count() < rows:
                grid_column.addStretch(1)

        # calculate new pane size
        geom = self.pane.geometry()
        geom.setWidth((num_columns * (MediaLibrary.THUMB_WIDTH + MediaLibrary.THUMB_SPACING)) + MediaLibrary.THUMB_SPACING)
        geom.setHeight((rows * (MediaLibrary.THUMB_HEIGHT + MediaLibrary.THUMB_SPACING)) + MediaLibrary.THUMB_SPACING)
        self.pane.setGeometry(geom)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = MediaLibrary()
    panel.show()
    sys.exit(app.exec_())
    app.quit()
