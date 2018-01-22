import typing

from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QPoint, QSize, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPixmapCache

from elapsed_timer import elapsed_timer
from slide_viewer_47.common.slide_tile import SlideTile


def qrectf_to_rect(qrectf: QRectF):
    if qrectf:
        return (int(qrectf.x()), int(qrectf.y()), int(qrectf.width()), int(qrectf.height()))





class MediaObjectListModel(QAbstractListModel):
    def __init__(self, media_objects=[], icon_size=None):
        super().__init__()
        self.media_objects = media_objects
        self.icon_size = icon_size

    def rowCount(self, parent=QModelIndex()):
        return len(self.media_objects)

    def data(self, index, role=Qt.DisplayRole):
        item = self.media_objects[index.row()]
        # if role == Qt.SizeHintRole:
            # w, h = item.data["icon_size"]
            # size = QSize(w*2, h)
            # print("SizeHintRole: ", size)
            # return QVariant()
        if role == Qt.FontRole:
            return QVariant()
        if role == Qt.DisplayRole:
            item.data["edit_role"] = False
            if "hide_decoration_role" in item.data:
                del item.data["hide_decoration_role"]
            suffix = "\nlevel: {}\nrect: {}".format(item.data["slide_tile"].level,
                                                         qrectf_to_rect(item.data["slide_tile"].rect))
            return QVariant(item.text + suffix)
        elif role == Qt.EditRole:
            item.data["hide_decoration_role"] = True
            item.data["edit_role"] = True
            return QVariant(item.data["slide_tile"])
        elif role == Qt.ToolTipRole:
            return QVariant(item.text)
        elif role == Qt.DecorationRole:
            # if "hide_decoration_role" in item.data:
            return QVariant()
            # w, h = self.icon_size
            # icon_pixmap = QPixmap(w, h)
            # painter = QPainter(icon_pixmap)
            # painter.fillRect(icon_pixmap.rect(), QColor(0, 255, 0))
            # painter.end()
            # return QVariant(icon_pixmap)
            item = item
            pilimg_or_pixmap = item.pilimg_or_pixmap
            w, h = self.icon_size
            img_key = item.text + "_{}_{}".format(w, h)
            pixmap = QPixmapCache.find(img_key)
            pixmap = None
            # print(img_key, pixmap)
            if not pixmap:
                # print("read")
                if pilimg_or_pixmap:
                    if callable(pilimg_or_pixmap):
                        # print(self.icon_size)
                        # pilimg_or_pixmap = pilimg_or_pixmap(self.icon_size)
                        pilimg_or_pixmap = pilimg_or_pixmap(item)
                    if not isinstance(pilimg_or_pixmap, QPixmap):
                        img = ImageQt(pilimg_or_pixmap)
                        pixmap = QtGui.QPixmap.fromImage(img).copy()
                    else:
                        pixmap = pilimg_or_pixmap
                    QPixmapCache.insert(img_key, pixmap)

            icon_pixmap = QPixmap(w, h)
            painter = QPainter(icon_pixmap)
            painter.fillRect(icon_pixmap.rect(), painter.background())
            scaled_pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
            p = QPoint((w - scaled_pixmap.width()) / 2, (h - scaled_pixmap.height()) / 2)
            painter.drawPixmap(p, scaled_pixmap)
            painter.end()

            return QVariant(icon_pixmap)
        elif role == Qt.UserRole:
            return QVariant(item.data)
        elif role == Qt.UserRole + 1:
            return QVariant(item)
        else:
            return QVariant()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def on_icon_size_changed(self, icon_size):
        self.icon_size = icon_size
        self.beginResetModel()
        self.endResetModel()
        # self.dataChanged.emit(self.index(0), self.index(0))

    def update_media_objects(self, media_objects):
        self.beginResetModel()
        QPixmapCache.clear()
        self.media_objects = media_objects
        self.endResetModel()

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        item = self.media_objects[index.row()]
        item.data["slide_tile"] = value
        return True
