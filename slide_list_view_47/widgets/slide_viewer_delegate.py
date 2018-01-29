import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QRectF
from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QGraphicsScene, QWidget

from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.widgets.slide_viewer_editor import SlideViewerEditor
from slide_viewer_47.common.screenshot_builders import build_screenshot_image
from slide_viewer_47.common.slide_view_params import SlideViewParams
from slide_viewer_47.common.slide_helper import SlideHelper
from slide_viewer_47.graphics.slide_graphics_group import SlideGraphicsGroup


class SlideViewerDelegate(QStyledItemDelegate):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)

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
            w = self.calculate_size(default_size.width(), w_expand)
            h = self.calculate_size(default_size.height(), h_expand)
        return QSize(w, h)

    def sizeHint(self, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> QtCore.QSize:
        # print("sizeHint() option.rect:", option.rect)
        size = super().sizeHint(option, index)
        # w, h = self.calculate_item_size(size, option, 1)
        w, h = index.data(SlideListModel.DecorationSizeOrRatioRole)
        decoration_size = QSize(w, h)
        custom_decoration_size = self.calculate_custom_decoration_size(size, option, decoration_size)
        if option.decorationPosition == QStyleOptionViewItem.Left:
            w = size.width()
            h = custom_decoration_size.height()
        elif option.decorationPosition == QStyleOptionViewItem.Top:
            w = custom_decoration_size.width()
            h = size.height() + custom_decoration_size.height()
        qsize = QSize(w, h)
        w, h = qsize.width(), qsize.height()
        # print("======sizeHint=====")
        # print("option.rect: ", option.rect)
        # print("new size: ", w, h)
        # print("====================")
        return qsize

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        default_size = option.rect.size()
        decoration_size = index.data(SlideListModel.DecorationSizeOrRatioRole)
        custom_decoration_size = self.calculate_custom_decoration_size(default_size, option, QSize(*decoration_size))
        if option.decorationPosition == QStyleOptionViewItem.Left:
            text_x, text_y = custom_decoration_size.width(), 0
            text_width = default_size.width() - custom_decoration_size.width()
            text_height = custom_decoration_size.height()
        elif option.decorationPosition == QStyleOptionViewItem.Top:
            text_x, text_y = 0, custom_decoration_size.height()
            text_width = custom_decoration_size.width()
            text_height = default_size.height() - custom_decoration_size.height()

        slide_view_params: SlideViewParams = index.data(SlideListModel.SlideViewParamsRole)
        scene_rect = QRectF(*slide_view_params.level_rect)
        img_key = "{}_{}_{}_{}_{}_{}_{}".format(slide_view_params.slide_path, custom_decoration_size, slide_view_params.level,
                                       slide_view_params.level_rect, id(slide_view_params.grid_rects_0_level),
                                       id(slide_view_params.grid_colors_0_level), slide_view_params.grid_visible)
        icon_pixmap = QPixmapCache.find(img_key)
        if icon_pixmap is None:
            # print("read", img_key)
            scene = QGraphicsScene()
            slide_graphics = SlideGraphicsGroup(slide_view_params)
            scene.clear()
            scene.invalidate()
            scene.addItem(slide_graphics)
            slide_graphics.update_visible_level(slide_view_params.level)
            slide_helper = SlideHelper(slide_view_params.slide_path)
            scene.setSceneRect(slide_helper.get_rect_for_level(slide_view_params.level))
            image = build_screenshot_image(scene, custom_decoration_size, scene_rect)
            icon_pixmap = QtGui.QPixmap.fromImage(image)
            QPixmapCache.insert(img_key, icon_pixmap)

        painter.fillRect(option.rect, painter.background())
        painter.drawPixmap(option.rect.topLeft(), icon_pixmap)
        # painter.drawRect(option.rect.topLeft().x(), option.rect.topLeft().y(), icon_pixmap.width(),
        #                  icon_pixmap.height())

        option.rect = option.rect.translated(text_x, text_y)
        option.rect.setSize(QSize(text_width, text_height))
        # print("rect:", option.rect)
        super().paint(painter, option, index)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> QWidget:
        # print(option.displayAlignment)
        # print(option.viewItemPosition)
        # print(option.decorationAlignment)
        # print(option.decorationPosition)
        slide_viewer_editor = SlideViewerEditor(parent, option.decorationPosition == QStyleOptionViewItem.Top)
        slide_viewer_editor.setGeometry(option.rect)
        slide_viewer_editor.setContentsMargins(0, 0, 0, 0)
        return slide_viewer_editor

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        if editor.slide_viewer.parent() and editor.slide_viewer.parent().layout():
            editor.slide_viewer.parent().layout().setContentsMargins(0, 0, 0, 0)
        super().updateEditorGeometry(editor, option, index)
