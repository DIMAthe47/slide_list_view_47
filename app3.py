import collections
import sys
import typing
from functools import lru_cache

import openslide
from PIL.ImageQt import ImageQt

from PyQt5.QtGui import QPixmapCache, QPainter
from PyQt5.QtCore import Qt, QRectF, QRect, QPoint, QSize
from PyQt5.QtWidgets import QAbstractItemView, QVBoxLayout, QGraphicsScene

from media_object import MediaObject
from media_object_main_window import MediaObjectMainWindow
from slide_viewer_47.common.slide_tile import SlideTile
from slide_viewer_47.common.utils import SlideHelper
from slide_viewer_47.graphics.slide_graphics_group import SlideGraphicsGroup
from slide_viewer_47.widgets.slide_viewer import SlideViewer, build_screenshot_image


def excepthook(excType, excValue, tracebackobj):
    print(excType, excValue, tracebackobj)


sys.excepthook = excepthook

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtProperty

from PyQt5.QtWidgets import QStyleOptionViewItem, QWidget, QApplication, QStyledItemDelegate, \
    QItemEditorCreatorBase


def qrectf_to_rect(qrectf: QRectF):
    if qrectf:
        return (int(qrectf.x()), int(qrectf.y()), int(qrectf.width()), int(qrectf.height()))


@lru_cache(maxsize=100)
def read_thumbnail(slide_path, thumbnail_size):
    slide = openslide.OpenSlide(slide_path)
    thumbnail = slide.get_thumbnail(thumbnail_size)
    return thumbnail


@lru_cache(maxsize=100)
def read_tile(slide_path, location, size, downsample):
    slide = openslide.OpenSlide(slide_path)
    level = slide.get_best_level_for_downsample(downsample)
    tile = slide.read_region(location, level, size)
    return tile


class SlideViewerEditorCreator(QItemEditorCreatorBase):

    def __init__(self) -> None:
        super().__init__()

    def valuePropertyName(self) -> QtCore.QByteArray:
        return b"slide_tile"

    def createWidget(self, parent: QWidget) -> QWidget:
        return SlideViewerEditor(parent)


class SlideViewerEditor(QWidget):

    # def slide_screenshot_image_painter(painter: QPainter, image_size, item: SlideTile):

    @pyqtProperty(SlideTile, user=True)
    def slide_tile(self) -> SlideTile:
        # downsample = self.slide_viewer.slide_helper.get_downsample_for_level(self.slide_viewer.current_level)
        # level = slide_helper.get_best_level_for_downsample(downsample)
        slide_tile = SlideTile(self._slide_tile.slide_path, self.slide_viewer.current_level,
                               self.slide_viewer.get_current_view_scene_rect())
        print("from viewer:", self.slide_viewer.current_level, self.slide_viewer.get_current_view_scene_rect())
        return slide_tile

    @slide_tile.setter
    def slide_tile(self, value: SlideTile):
        self._slide_tile = value
        start_level, start_rect = None, None
        slide_helper = SlideHelper(value.slide_path)
        if value.level and value.rect:
            start_level = value.level
            if isinstance(value.rect, collections.Iterable):
                start_rect = QRectF(*value.rect)
            else:
                start_rect = value.rect

        print("to viewer:", start_level, start_rect)
        self.slide_viewer.load_slide(value.slide_path, start_level, start_rect)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self._slide_tile = None
        self.slide_viewer = SlideViewer()
        self.setAutoFillBackground(True)
        layout = QVBoxLayout()
        # layout.addWidget(QTextEdit("123123"))
        layout.addWidget(self.slide_viewer)
        self.setLayout(layout)


class ItemDelegate(QStyledItemDelegate):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.custom_decoration_size_or_ratio = (300, 300)
        # self.custom_decoration_size_or_ratio = (0.25, 0.5)

    def calculate_expanded_dim(self, dim, expand):
        if isinstance(expand, float):
            expand *= dim
        expanded = dim + expand
        return expanded

    def calculate_size(self, dim, expand):
        if isinstance(expand, float):
            expand *= dim
        expanded = expand
        return expanded

    # def calculate_item_size(self, size: QSize, option: QStyleOptionViewItem, expand_coeff=1):
    #     w, h = size.width(), size.height()
    #     w_expand, h_expand = self.custom_decoration_size_or_ratio
    #     w_expand *= expand_coeff
    #     h_expand *= expand_coeff
    #     if option.decorationPosition == QStyleOptionViewItem.Left:
    #         w = self.calculate_expanded_dim(size.width(), w_expand)
    #     elif option.decorationPosition == QStyleOptionViewItem.Top:
    #         h = self.calculate_expanded_dim(size.height(), h_expand)
    #     return (w, h)

    def calculate_custom_decoration_size(self, size: QSize, option: QStyleOptionViewItem):
        w, h = size.width(), size.height()
        w_expand, h_expand = self.custom_decoration_size_or_ratio
        if option.decorationPosition == QStyleOptionViewItem.Left:
            w = self.calculate_size(size.width(), w_expand)
            h = self.calculate_size(size.height(), h_expand)
        elif option.decorationPosition == QStyleOptionViewItem.Top:
            h = self.calculate_size(size.height(), h_expand)
        return QSize(w, h)

    def sizeHint(self, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtCore.QSize:
        # print("sizeHint() option.rect:", option.rect)
        size = super().sizeHint(option, index)
        # w, h = self.calculate_item_size(size, option, 1)
        qsize = size + self.calculate_custom_decoration_size(size, option)
        w, h = qsize.width(), qsize.height()
        # print("======sizeHint=====")
        # print("option.rect: ", option.rect)
        # print("new size: ", w, h)
        # print("====================")
        return qsize

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        # print("option.rect: ", option.rect)
        # pilimg_or_pixmap = item.pilimg_or_pixmap
        # pilimg = pilimg_or_pixmap(item)
        # img = ImageQt(pilimg)
        # pixmap = QtGui.QPixmap.fromImage(img).copy()

        # w, h = item.data["icon_size"]
        # qsize = index.data(Qt.SizeHintRole)
        # qsize = self.sizeHint(option, index)
        qsize = option.rect.size()

        w, h = qsize.width(), qsize.height()
        # print("w,h: ", w, h)

        custom_decoration_size = self.calculate_custom_decoration_size(qsize, option)
        if option.decorationPosition == QStyleOptionViewItem.Left:
            w //= 2
            dx, dy = custom_decoration_size.width(), 0
            nw, ny = qsize.width() - custom_decoration_size.width(), qsize.height()
            # sx, sy = 1 / 2, 1
        elif option.decorationPosition == QStyleOptionViewItem.Top:
            h //= 2
            dx, dy = 0, custom_decoration_size.height()
            nw, ny = qsize.width(), qsize.height() - custom_decoration_size.height(),
            # sx, sy = 1, 1 / 2
        # h = 200

        w, h = custom_decoration_size.width(), custom_decoration_size.height()

        scene = QGraphicsScene()
        scene.clear()
        item = index.data(Qt.UserRole + 1)
        slide_tile: SlideTile = item.data["slide_tile"]
        slide_graphics = SlideGraphicsGroup(slide_tile.slide_path)
        scene.addItem(slide_graphics)
        level = slide_tile.level
        rect = slide_tile.rect
        slide_helper = SlideHelper(slide_tile.slide_path)
        if level == None:
            level = slide_helper.get_max_level()
            rect = QRectF(0, 0, *slide_helper.get_level_size(level))
        else:
            print("stop here")
        slide_graphics.update_visible_level(level)
        scene.setSceneRect(slide_helper.get_rect_for_level(level))

        image = build_screenshot_image(scene, QSize(w, h), rect)
        pixmap = QtGui.QPixmap.fromImage(image)
        # pixmap.save("img.jpg")

        painter.fillRect(option.rect, painter.background())
        painter.drawPixmap(option.rect.topLeft(), pixmap)

        # icon_pixmap = QPixmap(w, h)
        # painter.fillRect(icon_pixmap.rect(), painter.background())
        # scaled_pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        # scaled_pixmap = pixmap.scaled(w, h, Qt.IgnoreAspectRatio)
        # p = QPoint((w - scaled_pixmap.width()) / 2, (h - scaled_pixmap.height()) / 2)
        # painter.drawPixmap(p, scaled_pixmap)
        # painter.drawPixmap(option.rect.topLeft(), scaled_pixmap)

        option.rect = option.rect.translated(dx, dy)
        option.rect.setSize(QSize(nw, ny))
        # print("rect:", option.rect)
        super().paint(painter, option, index)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> QWidget:
        # option.decorationPosition = QStyleOptionViewItem.Right
        # option.decorationSize = QSize(270, 200)
        # return super().createEditor(parent, option, index)
        # print(option.displayAlignment)
        # print(option.viewItemPosition)
        # print(option.decorationAlignment)
        # print(option.decorationPosition)
        slide_viewer_editor = SlideViewerEditor(parent)
        slide_viewer_editor.setGeometry(option.rect)
        slide_viewer_editor.setContentsMargins(0, 0, 0, 0)
        return slide_viewer_editor

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        if editor.slide_viewer.parent() and editor.slide_viewer.parent().layout():
            editor.slide_viewer.parent().layout().setContentsMargins(0, 0, 0, 0)
        super().updateEditorGeometry(editor, option, index)


def main():
    app = QApplication(sys.argv)
    win = MediaObjectMainWindow()
    cache_size_in_kb = 300 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)
    # factory = QItemEditorFactory()
    # editorCreator = SlideViewerEditorCreator()
    # factory.registerEditor(QVariant(SlideTile()).userType(), editorCreator)
    # QItemEditorFactory.setDefaultFactory(factory)

    filepathes = [
        r'C:\Users\DIMA\PycharmProjects\slide_cbir_47\downloads\images\19403.svs',
        # r'C:\Users\DIMA\Downloads\11096.svs'
    ]

    def img_func(item):
        slide_tile = item.data["slide_tile"]

        # downsample = item.data["slide_tile"].downsample
        level = item.data["slide_tile"].level
        qrect = item.data["slide_tile"].rect
        # if level and qrect:
        # size = (rect[2] - rect[0], rect[3] - rect[1])
        # qrect_0_level = QRect(QPoint(qrect.topLeft().toPoint()) * downsample, qrect.size().toSize())
        # rect_0_level = qrectf_to_rect(qrect_0_level)
        # tile = read_tile(slide_tile.slide_path, rect_0_level[0:2], rect_0_level[2:4], downsample)
        # else:
        tile = read_thumbnail(slide_tile.slide_path, (300, 300))
        return tile

    slide_tiles = [
        MediaObject(filepath, img_func, {"slide_tile": SlideTile(filepath), "icon_size": (2000, 200)}) for filepath in
        filepathes
    ]

    win.media_objects_widget.list_model.update_media_objects(slide_tiles)
    win.media_objects_widget.list_view.setEditTriggers(
        QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)

    win.media_objects_widget.list_view.update_icon_max_size_or_ratio((200, 200))

    win.media_objects_widget.list_view.setItemDelegate(ItemDelegate())

    win.media_objects_widget.list_view.setMouseTracking(True)

    # def f1(e):
    #     print(e)

    # win.media_objects_widget.list_view.wheelEventSignal.connect(f1)

    # win.media_objects_widget.list_view.viewOptions().decorationPosition = QStyleOptionViewItem.Right
    # win.media_objects_widget.list_view.setStyle(win.media_objects_widget.list_view.viewOptions())
    # win.media_objects_widget.list_view.setStyle(win.media_objects_widget.list_view.viewOptions())

    win.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
