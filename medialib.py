import sys
import os
import json
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
from medialib.service import ImportJson
from medialib.model import TableBase, Media

Cover.COVER_PATH = '/data/Media/Movies/Children/Covers/'

class MediaLibrary(QMainWindow):
    MOVIES = '/data/Media/Movies/Children/'
    THUMB_WIDTH = 143
    THUMB_HEIGHT = 200
    THUMB_SPACING = 7

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self._create_menu_bar()

        # build table
        table = CoverTable(width=self.THUMB_WIDTH, height=self.THUMB_HEIGHT, spacing=self.THUMB_SPACING)
        for cover in self._fetch_covers():
            table.add(cover)

        # add scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidget(table)
        scrollArea.setWidgetResizable(True)

        # add scrollArea to window
        self.setCentralWidget(scrollArea)
        self.resize(1375, 800)
        self.center()
        self.setWindowTitle('Media Library')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _create_menu_bar(self):
        updateAction = QAction('Update...', self)
        updateAction.setStatusTip('Update to latest version')
        updateAction.triggered.connect(self._update)

        quitAction = QAction('Quit', self)
        quitAction.setShortcut('Ctrl Q')
        quitAction.setStatusTip('Quit application')
        quitAction.triggered.connect(self.close)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(updateAction)
        fileMenu.addSeparator()
        fileMenu.addAction(quitAction)

    def _update(self):
        try:

            print('Updating code ...')
            output = subprocess.check_output(['/usr/bin/git', 'pull', '--rebase'], stderr=subprocess.STDOUT)
            print('Code updated: [%s]' % output)

        except subprocess.CalledProcessError as perror:
            print('Error updating source, return code (%s)\n[%s]' % (perror.returncode, perror.output))
            return

        print('Wiping database ...')
        try:
            os.unlink('medialib.db')
        except OSError: pass

        try:
            os.unlink('medialib.db-journal')
        except OSError: pass

        print('Loading database ...')
        engine = create_engine('sqlite:///medialib.db', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()

        TableBase.metadata.create_all(engine)
        session.flush()

        json_import = ImportJson(session)
        datafile = open('medialib.json', 'r')
        objects = json.load(datafile, object_hook=json_import.to_media_object)

        session.flush()
        session.commit()

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
