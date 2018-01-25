import openslide
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QVariant, QSize, Qt, QPoint
from PyQt5.QtGui import QPixmapCache, QImage, QPainter, QPixmap


def str_display_func(item):
    return str(item)


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

    return icon_pixmap


def item_func(item):
    return item


def decoration_size_hint_func(size_else_ratio=True):
    icon_size = (200, 200)
    return icon_size