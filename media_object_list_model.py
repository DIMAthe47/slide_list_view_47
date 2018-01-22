import typing

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QPoint, QSize, QRectF, QSizeF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPixmapCache, QImage


def str_display_func(item):
    return QVariant(str(item))


def imagepath_decoration_func(filepath, icon_size: QSize):
    pilimg: Image.Image = Image.open(filepath)
    img_key = filepath + "_{}".format(str(icon_size))
    icon_pixmap = QPixmapCache.find(img_key)
    if icon_pixmap is None:
        icon_pixmap = QPixmap(icon_size)
        painter = QPainter(icon_pixmap)
        painter.fillRect(icon_pixmap.rect(), painter.background())
        scaled_icon_image = ImageQt(pilimg).scaled(icon_size, Qt.KeepAspectRatio)
        p = QPoint((icon_size.width() - scaled_icon_image.width()) / 2,
                   (icon_size.height() - scaled_icon_image.height()) / 2)
        painter.drawImage(p, scaled_icon_image)
        painter.end()
        QPixmapCache.insert(img_key, icon_pixmap)

    return QVariant(icon_pixmap)


def item_func(item):
    return item


def size_hit_func(item):
    return QVariant(QSize(200, 200))


class MediaObjectListModel(QAbstractListModel):
    def __init__(self, items=[], display_func=str_display_func, decoration_func=None,
                 edit_func=None, tooltip_func=str_display_func,
                 size_hint_func=None, user_func=item_func):
        super().__init__()
        self.items = items
        self.display_func = display_func
        self.decoration_func = decoration_func
        self.size_func = size_hint_func
        self.edit_func = edit_func

        self.role_func = {
            Qt.SizeHintRole: size_hint_func,
            Qt.DisplayRole: display_func,
            Qt.EditRole: edit_func,
            Qt.ToolTipRole: tooltip_func,
            Qt.DecorationRole: decoration_func,
            Qt.UserRole: user_func,
        }

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        item = self.items[index.row()]
        if role in self.role_func:
            custom_handler = self.role_func[role]
            if custom_handler:
                if role == Qt.DecorationRole:
                    icon_size = self.data(index, Qt.SizeHintRole)
                    return custom_handler(item, icon_size.value())
                else:
                    return custom_handler(item)
        return QVariant()

    def flags(self, index):
        if self.edit_func:
            return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def on_icon_size_changed(self, icon_size):
        self.icon_size = icon_size
        self.beginResetModel()
        self.endResetModel()
        # self.dataChanged.emit(self.index(0), self.index(0))

    def update_media_objects(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def setData(self, index: QModelIndex, value: typing.Any, role=Qt.DisplayRole) -> bool:
        item = self.items[index.row()]
        if role == Qt.UserRole:
            self.items[index.row()] = value
            self.dataChanged(index, index)
            return True
        return False
