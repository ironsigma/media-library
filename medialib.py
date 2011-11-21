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
        self.settings = QSettings('IzyLab', 'MediaLib')
        self._check_db_update()
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
        self.setStatusBar(QStatusBar())
        menubar = self.menuBar()

        # file
        fileMenu = menubar.addMenu('&File')

        aboutAction = QAction('About...', self)
        aboutAction.setStatusTip('About Media Library')
        aboutAction.triggered.connect(self._about)
        fileMenu.addAction(aboutAction)

        fileMenu.addSeparator()

        updateAction = QAction('Update', self)
        updateAction.setStatusTip('Update to latest version')
        updateAction.triggered.connect(self._update)
        fileMenu.addAction(updateAction)

        # view
        viewMenu = menubar.addMenu('&View')

        # rating
        ratingMenu = viewMenu.addMenu('&Rating')

        gRatingAction = QAction('G', self)
        gRatingAction.setCheckable(True)
        gRatingAction.setChecked(True)
        ratingMenu.addAction(gRatingAction)

        pgRatingAction = QAction('PG', self)
        pgRatingAction.setCheckable(True)
        ratingMenu.addAction(pgRatingAction)

        pg13RatingAction = QAction('PG-13', self)
        pg13RatingAction.setCheckable(True)
        ratingMenu.addAction(pg13RatingAction)

        # types
        typeMenu = viewMenu.addMenu('&Type')

        movieAction = QAction('Movies', self)
        movieAction.setCheckable(True)
        movieAction.setChecked(True)
        typeMenu.addAction(movieAction)

        showAction = QAction('Shows', self)
        showAction.setCheckable(True)
        movieAction.setChecked(True)
        typeMenu.addAction(showAction)

    def _update(self):
        try:

            print('Updating code ...')
            output = subprocess.check_output(['/usr/bin/git', 'pull', '--rebase'],
                    stderr=subprocess.STDOUT).decode('utf-8')

        except subprocess.CalledProcessError as perror:
            self._show_dialog_message('Program Update', 'Error updating program files.',
                    'Return code: %s\nOutput:\n%s' % (perror.returncode, perror.output.decode('utf-8')))
            return

        self.settings.setValue('update_db', True)

        self._show_dialog_message('Program Update',
                'Update completed and will now restart.', 'Output:\n%s' % output,
                QMessageBox.Information)

        self._restart()

    def _check_db_update(self):
        if not self.settings.contains('update_db'):
            print('No DB update required')
            return

        print('Wiping database ...')

        if os.path.isfile('medialib.db'):
            try:
                os.unlink('medialib.db')
            except OSError:
                print('Unable to delete DB')
                sys.exit(1)

        if os.path.isfile('medialib.db-journal'):
            try:
                os.unlink('medialib.db-journal')
            except OSError:
                print('Unable to delete DB journal')
                sys.exit(1)

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
        session.close()
        self.settings.remove('update_db')
        print('DB is good to go')

    def _show_dialog_message(self, title, message, details, type=QMessageBox.Critical):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setDetailedText(details)
        msgBox.exec_()

    def _restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def _about(self):
        version = open('VERSION', 'r').read()
        QMessageBox.about(self, 'Media Library', version)
 
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
        args = ['/usr/bin/totem', '--replace']
        for f in media.files:
            args.append(MediaLibrary.MOVIES + f.filename)
        subprocess.Popen(args)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = MediaLibrary()
    panel.show()
    sys.exit(app.exec_())
    app.quit()
