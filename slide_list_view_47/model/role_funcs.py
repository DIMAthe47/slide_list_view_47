import openslide
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import QVariant, QSize, Qt, QPoint
from PyQt5.QtGui import QPixmapCache, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsView

from slide_viewer_47.common.slide_view_params import SlideViewParams


def slideviewparams_to_str(item: any):
    return item.slide_path


def slidepath_to_pximap(slidepath, icon_size: QSize):
    img_key = "{}_{}".format(slidepath, str(icon_size))
    icon_pixmap = QPixmapCache.find(img_key)
    if icon_pixmap is None:
        # pilimg: Image.Image = Image.open(slidepath)
        with openslide.open_slide(slidepath) as slide:
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


def item_to_pixmap_through_slideviewparams_factory(item_to_slideviewparams):
    def item_to_pixmap(item, icon_size: QSize):
        slide_view_params = item_to_slideviewparams(item)
        return slideviewparams_to_pixmap(slide_view_params, icon_size)

    return item_to_pixmap


def slideviewparams_to_pixmap(slide_view_params: SlideViewParams, icon_size: QSize):
    return slidepath_to_pximap(slide_view_params.slide_path, icon_size)


def item_func(item):
    return item


# def item_setter(items, index, value):
#     items[index.row()] = value

def decoration_size_hint_func(size_else_ratio=True):
    icon_size = (200, 200)
    return icon_size


def slidepath_to_slideviewparams(slidepath):
    return SlideViewParams(slidepath)


def decoration_size_func_factory(view: QGraphicsView, width_or_ratio, height_or_ratio):
    w = width_or_ratio
    h = height_or_ratio

    def decoration_size_func(size_else_ratio=True):
        viewport_size = view.viewport().size()
        if isinstance(w, float):
            icon_width = viewport_size.width() * w - view.spacing() * 2 - 4
        else:
            icon_width = w
        if isinstance(h, float):
            icon_height = viewport_size.height() * h - view.spacing() * 2 - 4
        else:
            icon_height = h

        if size_else_ratio:
            icon_size = (icon_width, icon_height)
        else:
            icon_size = (w, h)

        return icon_size

    return decoration_size_func
