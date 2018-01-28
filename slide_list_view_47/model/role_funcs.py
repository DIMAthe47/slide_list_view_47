import openslide
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QVariant, QSize, Qt, QPoint
from PyQt5.QtGui import QPixmapCache, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsView

from slide_viewer_47.common.slide_view_params import SlideViewParams


def str_display_func(item):
    return str(item)


def slideviewparams_to_str(item: SlideViewParams):
    return item.slide_path


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


def slideviewparams_decoration_func(slide_view_params: SlideViewParams, icon_size: QSize):
    return imagepath_decoration_func(slide_view_params.slide_path, icon_size)


def item_func(item):
    return item


def decoration_size_hint_func(size_else_ratio=True):
    icon_size = (200, 200)
    return icon_size


def filepath_to_slideviewparams(filepath):
    return SlideViewParams(filepath)


def decoration_size_func_factory(view: QGraphicsView, width_or_ratio, height_or_ratio):
    w = width_or_ratio
    h = height_or_ratio

    def decoration_size_func(size_else_ratio=True):
        viewport_size = view.viewport().size()
        if isinstance(w, float):
            icon_width = viewport_size.width() * w - view.spacing() * 2 - 2
        else:
            icon_width = w
        if isinstance(h, float):
            icon_height = viewport_size.height() * h - view.spacing() * 2 - 2
        else:
            icon_height = h

        if size_else_ratio:
            icon_size = (icon_width, icon_height)
        else:
            icon_size = (w, h)

        return icon_size

    return decoration_size_func
