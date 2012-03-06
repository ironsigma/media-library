import sys
import os
import subprocess

# UI
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from medialib.ui import Cover
from medialib.ui import CoverTable
from medialib.service import scan_dir

class MediaLibrary(QMainWindow):
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
        self._center()
        self.setWindowTitle('Media Library')

    def _center(self):
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

    def _update(self):
        try:

            print('Updating code ...')
            output = subprocess.check_output(['/usr/bin/git', 'pull', '--rebase'],
                    stderr=subprocess.STDOUT).decode('utf-8')

        except subprocess.CalledProcessError as perror:
            self._show_dialog_message('Program Update', 'Error updating program files.',
                    'Return code: %s\nOutput:\n%s' % (perror.returncode, perror.output.decode('utf-8')))
            return

        self._show_dialog_message('Program Update',
                'Update completed and will now restart.', 'Output:\n%s' % output,
                QMessageBox.Information)

        self._restart()

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

        medialist = scan_dir('/home/Isabelle/Movies')

        # fetch movies and create covers
        for media in medialist:
            if media.rating != 'G':
                continue

            cover = Cover(self, media, MediaLibrary.THUMB_WIDTH, MediaLibrary.THUMB_HEIGHT)
            cover.clicked.connect(self._start_movie)
            cover_list.append(cover)

        return cover_list

    def _start_movie(self):
        media = self.sender().media
        args = ['/usr/bin/totem', '--replace']
        for f in media.files:
            args.append(f)
        subprocess.Popen(args)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = MediaLibrary()
    panel.show()
    sys.exit(app.exec_())
    app.quit()
