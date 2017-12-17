from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPen, QBrush


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
        for i, tile_rect in enumerate(self.tile_rects):
            pen = QPen(QColor(0, 0, 0, 0))
            brush = QBrush(self.qcolors[i])
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect(QRectF(*tile_rect))
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
