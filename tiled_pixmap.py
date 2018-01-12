import itertools
import math
import random

from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPen, QBrush

from elapsed_timer import elapsed_timer


class TiledPixmap(QPixmap):
    def __init__(self, pilimg_or_path, tile_rects, qcolors: list) -> None:
        img = ImageQt(pilimg_or_path)
        pixmap = QtGui.QPixmap.fromImage(img)
        self.original_pixmap = pixmap
        super().__init__(pixmap)
        self.tile_rects = tile_rects
        self.fill(QColor(0, 0, 0, 255))
        self.qcolors = qcolors
        self.mask_on()

    def mask_on(self):
        painter = QPainter(self)
        painter.save()
        painter.drawPixmap(self.rect(), self.original_pixmap)
        pen = QPen(QColor(0, 0, 0, 0))
        painter.setPen(pen)
        with elapsed_timer() as elapsed:
            for i, tile_rect in enumerate(self.tile_rects):
                brush = QBrush(self.qcolors[i])
                painter.setBrush(brush)
                painter.drawRect(QRectF(*tile_rect))
            print("rects elapsed:", elapsed())

            # qcolor = self.qcolors[i]
            # painter.drawText(QRect(*tile_rect), Qt.AlignCenter, str(qcolor.alpha()))
            # painter.drawText(QRect(*tile_rect), Qt.AlignBottom, str(i))
            # painter.fillRect(*tile_rect, self.qcolors[i])
        painter.restore()
        painter.end()

    def mask_off(self):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.original_pixmap)
        painter.end()


def chop(length, n_chops):
    regular_chop_length = math.ceil(length / n_chops)
    chops = [regular_chop_length * i for i in range(n_chops)]
    offsets = [min((length - i * regular_chop_length, regular_chop_length)) for i in range(n_chops)]
    return chops, offsets


def repeat_each_n_times(iterable, n):
    repeated_iter = zip(*[iter(iterable) for i in range(n)])
    return itertools.chain.from_iterable(repeated_iter)


def tile_rect(width, height, columns, rows):
    x_poses, widths = chop(width, columns)
    y_poses, heights = chop(height, rows)
    x_iter = itertools.cycle(x_poses)
    width_iter = itertools.cycle(widths)
    y_iter = repeat_each_n_times(y_poses, columns)
    height_iter = repeat_each_n_times(heights, columns)
    tiles_rects = list(zip(x_iter, y_iter, width_iter, height_iter))
    return tiles_rects


def chess_positions(columns, rows):
    return [(i, j) for i in range(rows) for j in range(columns) if (i + j) % 2 != 0]


def random_qcolor(alpha):
    return QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)
