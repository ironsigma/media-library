from PyQt4.QtGui import QLabel, QPixmap, QImage
from PyQt4.QtCore import Qt, pyqtSignal

class Cover(QLabel):
    COVER_PATH = 'covers/'

    clicked = pyqtSignal()

    def __init__(self, parent=None, media=None, width=143, height=200):
        super(self.__class__, self).__init__(parent)
        self.media = media
        self.setToolTip('%s (%s)' % (media.title, media.release))
        self.setPixmap(QPixmap.fromImage(QImage(Cover.COVER_PATH + self.media.cover).scaled(width, height,
            transformMode=Qt.SmoothTransformation)))

    def mouseReleaseEvent(self, ev):
        self.clicked.emit()
