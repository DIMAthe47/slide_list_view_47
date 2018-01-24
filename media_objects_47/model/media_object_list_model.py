import typing

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QPoint, QSize, QRectF, QSizeF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPixmapCache, QImage
import openslide


def str_display_func(item):
    return QVariant(str(item))


def imagepath_decoration_func(filepath, icon_size: QSize):
    img_key = filepath + "_{}".format(str(icon_size))
    icon_pixmap = QPixmapCache.find(img_key)
    if icon_pixmap is None:
        # pilimg: Image.Image = Image.open(filepath)
        with openslide.open_slide(filepath) as slide:
            pilimg = slide.get_thumbnail((icon_size.width(), icon_size.height()))
            icon_image = QImage(icon_size, QImage.Format_RGB888)
            painter = QPainter(icon_image)
            painter.fillRect(icon_image.rect(), painter.background())
            img = ImageQt(pilimg)
            scaled_icon_image = img.scaled(icon_size, Qt.KeepAspectRatio)
            p = QPoint((icon_size.width() - scaled_icon_image.width()) / 2,
                       (icon_size.height() - scaled_icon_image.height()) / 2)
            painter.drawImage(p, scaled_icon_image)
            painter.end()
            icon_pixmap = QPixmap.fromImage(icon_image)
            QPixmapCache.insert(img_key, icon_pixmap)

    return QVariant(icon_pixmap)


def item_func(item):
    return QVariant(item)


def decoration_size_hint_func(size_else_ratio=True):
    icon_size = (200, 200)
    return QVariant(icon_size)


class MediaObjectListModel(QAbstractListModel):
    ItemRole = Qt.UserRole
    DecorationSizeOrRatioRole = Qt.UserRole + 1

    def __init__(self, items=[], display_func=str_display_func, decoration_func=None,
                 edit_func=None, tooltip_func=str_display_func,
                 size_hint_func=None, item_func=item_func, decoration_size_hint_func=decoration_size_hint_func):
        super().__init__()
        self.items = items

        self.role_func = {
            Qt.SizeHintRole: size_hint_func,
            Qt.DisplayRole: display_func,
            Qt.EditRole: edit_func,
            Qt.ToolTipRole: tooltip_func,
            Qt.DecorationRole: decoration_func,
            MediaObjectListModel.ItemRole: item_func,
            MediaObjectListModel.DecorationSizeOrRatioRole: decoration_size_hint_func,
        }

    def update_role_func(self, role, func):
        self.role_func[role] = func

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        item = self.items[index.row()]
        if role in self.role_func:
            custom_handler = self.role_func[role]
            if custom_handler:
                if role == Qt.DecorationRole:
                    icon_size = self.data(index, MediaObjectListModel.DecorationSizeOrRatioRole)
                    return custom_handler(item, QSize(*icon_size.value()))
                elif role == MediaObjectListModel.DecorationSizeOrRatioRole:
                    icon_size = custom_handler()
                    return QVariant(icon_size)
                else:
                    return custom_handler(item)
        return QVariant()

    def flags(self, index):
        if self.role_func[Qt.EditRole] is not None:
            return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def update_media_objects(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def setData(self, index: QModelIndex, value: typing.Any, role=Qt.DisplayRole) -> bool:
        item = self.items[index.row()]
        if role == MediaObjectListModel.ItemRole:
            self.items[index.row()] = value
            self.dataChanged(index, index)
            return True
        return False
