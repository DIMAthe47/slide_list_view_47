import typing
from functools import lru_cache

import openslide
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QRectF
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QGraphicsScene, QWidget

from media_objects_47.model.media_object_list_model import MediaObjectListModel
from media_objects_47.widgets.slide_viewer_editor import SlideViewerEditor
from slide_viewer_47.common.screenshot_builders import build_screenshot_image
from slide_viewer_47.common.slide_tile import SlideTile
from slide_viewer_47.common.utils import SlideHelper
from slide_viewer_47.graphics.slide_graphics_group import SlideGraphicsGroup


class SlideViewerDelegate(QStyledItemDelegate):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
        # self.custom_decoration_size_or_ratio = (300, 300)
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

    def calculate_custom_decoration_size(self, default_size: QSize, option: QStyleOptionViewItem,
                                         decoration_size: QSize):
        w, h = default_size.width(), default_size.height()
        w_expand, h_expand = decoration_size.width(), decoration_size.height()
        if option.decorationPosition == QStyleOptionViewItem.Left:
            w = self.calculate_size(default_size.width(), w_expand)
            h = self.calculate_size(default_size.height(), h_expand)
        elif option.decorationPosition == QStyleOptionViewItem.Top:
            h = self.calculate_size(default_size.height(), h_expand)
        return QSize(w, h)

    def sizeHint(self, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> QtCore.QSize:
        # print("sizeHint() option.rect:", option.rect)
        size = super().sizeHint(option, index)
        # w, h = self.calculate_item_size(size, option, 1)
        w, h = index.data(MediaObjectListModel.DecorationSizeOrRatioRole)
        decoration_size = QSize(w, h)
        qsize = size + self.calculate_custom_decoration_size(size, option, decoration_size)
        w, h = qsize.width(), qsize.height()
        # print("======sizeHint=====")
        # print("option.rect: ", option.rect)
        # print("new size: ", w, h)
        # print("====================")
        return qsize

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        default_size = option.rect.size()
        decoration_size = index.data(MediaObjectListModel.DecorationSizeOrRatioRole).value()
        custom_decoration_size = self.calculate_custom_decoration_size(default_size, option, decoration_size)
        if option.decorationPosition == QStyleOptionViewItem.Left:
            text_x, text_y = custom_decoration_size.width(), 0
            text_width, text_height = default_size.width() - custom_decoration_size.width(), default_size.height()
        elif option.decorationPosition == QStyleOptionViewItem.Top:
            text_x, text_y = 0, custom_decoration_size.height()
            text_width, text_height = default_size.width(), default_size.height() - custom_decoration_size.height(),

        scene = QGraphicsScene()
        slide_tile: SlideTile = index.data(MediaObjectListModel.ItemRole)
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

        image = build_screenshot_image(scene, custom_decoration_size, rect)
        pixmap = QtGui.QPixmap.fromImage(image)
        # pixmap.save("img.jpg")

        painter.fillRect(option.rect, painter.background())
        painter.drawPixmap(option.rect.topLeft(), pixmap)

        option.rect = option.rect.translated(text_x, text_y)
        option.rect.setSize(QSize(text_width, text_height))
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

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        if editor.slide_viewer.parent() and editor.slide_viewer.parent().layout():
            editor.slide_viewer.parent().layout().setContentsMargins(0, 0, 0, 0)
        super().updateEditorGeometry(editor, option, index)


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
