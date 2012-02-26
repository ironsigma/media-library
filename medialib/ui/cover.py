from PyQt4.QtGui import QLabel, QPixmap, QImage
from PyQt4.QtCore import Qt, pyqtSignal

class Cover(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, media=None, width=143, height=200):
        super(self.__class__, self).__init__(parent)
        self.media = media
        self.setToolTip(media.title)
        self.setPixmap(QPixmap.fromImage(QImage(self.media.cover).scaled(width, height,
            transformMode=Qt.SmoothTransformation)))

    def mouseReleaseEvent(self, ev):
        self.clicked.emit()
