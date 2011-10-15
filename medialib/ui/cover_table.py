from PyQt4.QtGui import QWidget, QSizePolicy
from PyQt4.QtCore import QSize

class CoverTable(QWidget):

    def __init__(self, parent=None, width=145, height=200, spacing=10):
        super(self.__class__, self).__init__(parent)
        self._item_width = width
        self._item_height = height
        self._item_spacing = spacing

        self._item_list = []
        self._curr_num_cols = 0
        self._size_hint = QSize(0, 0)
        self._min_size_hint = QSize(width, height)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

    def resizeEvent(self, event):
        width = event.size().width()

        # if number of columns haven't changed skip change
        columns = width // (self._item_width + self._item_spacing)
        if self._curr_num_cols == columns:
            return

        # save new number of columns
        self._curr_num_cols = columns

        # init origin
        x = self._item_spacing
        y = self._item_spacing

        # lay each item
        for item in self._item_list:
            # if not the first column...
            if x != self._item_spacing:
                # calculate to see if we have enough space left in the window
                next_x_pos = x + self._item_spacing + self._item_width
                if next_x_pos > width:
                    # not enough space, move to the next row
                    x = self._item_spacing
                    y += self._item_spacing + self._item_height

            # relocate item and calculate next position
            item.move(x, y)
            x += self._item_spacing + self._item_width

        # update hint size
        self._size_hint.setWidth(x)
        self._size_hint.setHeight(y + self._item_spacing + self._item_height)

        # update min hint size and notify of geometry changes
        self._min_size_hint.setHeight(self._size_hint.height())
        self.updateGeometry()

    def add(self, item):
        item.setParent(self)
        self._item_list.append(item)
        self.update()

    def sizeHint(self):
        return self._size_hint

    def minimumSizeHint(self):
        return self._min_size_hint
