from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPixmapCache


class MediaObjectListModel(QAbstractListModel):
    def __init__(self, media_objects=[], icon_size=None):
        super().__init__()
        self.media_objects = media_objects
        self.icon_size = icon_size
        self.img_key__pixmap = {}
        self.img_key__cache_key = {}
        # self.key__icon={}
        self.img_key = "12345"

    def rowCount(self, parent=QModelIndex()):
        return len(self.media_objects)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return QVariant(self.media_objects[index.row()].text)
        elif role == Qt.EditRole:
            return QVariant(self.media_objects[index.row()].text)
        elif role == Qt.ToolTipRole:
            return QVariant(self.media_objects[index.row()].text)
        elif role == Qt.DecorationRole:
            pilimg_or_pixmap = self.media_objects[index.row()].pilimg_or_pixmap
            w, h = self.icon_size

            # img_key = self.media_objects[index.row()].text + "_{}_{}".format(w, h)
            pixmap = QPixmapCache.find(self.img_key)
            print(self.img_key, pixmap)
            # pixmap=None
            if not pixmap:
                # print("read")
                if pilimg_or_pixmap:
                    if callable(pilimg_or_pixmap):
                        print(self.icon_size)
                        pilimg_or_pixmap = pilimg_or_pixmap(self.icon_size)
                    if not isinstance(pilimg_or_pixmap, QPixmap):
                        img = ImageQt(pilimg_or_pixmap)
                        pixmap = QtGui.QPixmap.fromImage(img)
                    else:
                        pixmap = pilimg_or_pixmap
                QPixmapCache.insert(self.img_key, pixmap)
                self.img_key__pixmap[self.img_key] = pixmap

            icon_pixmap = QPixmap(w, h)
            painter = QPainter(icon_pixmap)
            painter.fillRect(icon_pixmap.rect(), painter.background())
            scaled_pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
            p = QPoint((w - scaled_pixmap.width()) / 2, (h - scaled_pixmap.height()) / 2)
            painter.drawPixmap(p, scaled_pixmap)
            painter.end()
            return QVariant(icon_pixmap)
        elif role == Qt.UserRole:
            return QVariant(self.media_objects[index.row()].data)
        else:
            return QVariant()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def on_icon_size_changed(self, icon_size):
        self.icon_size = icon_size
        self.dataChanged.emit(self.index(0), self.index(0))

    def update_media_objects(self, media_objects):
        self.beginResetModel()
        QPixmapCache.clear()
        self.media_objects = media_objects
        self.endResetModel()
