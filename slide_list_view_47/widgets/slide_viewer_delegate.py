import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QRectF, QSizeF
from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QGraphicsScene, QWidget

from elapsed_timer import elapsed_timer
from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.widgets.slide_viewer_editor import SlideViewerEditor
from slide_viewer_47.common.screenshot_builders import build_screenshot_image
from slide_viewer_47.common.slide_view_params import SlideViewParams
from slide_viewer_47.common.slide_helper import SlideHelper
from slide_viewer_47.graphics.slide_graphics_group import SlideGraphicsGroup


class SlideViewerDelegate(QStyledItemDelegate):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = None) -> None:
        super().__init__(parent)
        self.icon_and_text_spacing = 4

    def calculate_size(self, item_length, decoration_length_or_ratio):
        if isinstance(decoration_length_or_ratio, float):
            decoration_length_or_ratio *= item_length
        new_item_length = decoration_length_or_ratio
        return new_item_length

    def calculate_custom_decoration_size(self, item_size: QSize, option: QStyleOptionViewItem,
                                         decoration_size: QSize):
        w, h = item_size.width(), item_size.height()
        decoration_w_or_ratio, decoration_h_or_ratio = decoration_size.width(), decoration_size.height()
        if option.decorationPosition == QStyleOptionViewItem.Left:
            w = self.calculate_size(item_size.width(), decoration_w_or_ratio)
            h = self.calculate_size(item_size.height(), decoration_h_or_ratio)
        elif option.decorationPosition == QStyleOptionViewItem.Top:
            w = self.calculate_size(item_size.width(), decoration_w_or_ratio)
            h = self.calculate_size(item_size.height(), decoration_h_or_ratio)
        return QSize(w, h)

    def sizeHint(self, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> QtCore.QSize:
        # print("sizeHint() option.rect:", option.rect)
        item_size = super().sizeHint(option, index)
        # w, h = self.calculate_item_size(size, option, 1)
        item_new_w, item_new_h = index.data(SlideListModel.DecorationSizeOrRatioRole)
        custom_decoration_size = QSize(item_new_w, item_new_h)

        if option.decorationPosition == QStyleOptionViewItem.Left:
            item_new_w = item_size.width()
            item_new_h = custom_decoration_size.height()
        elif option.decorationPosition == QStyleOptionViewItem.Top:
            item_new_w = custom_decoration_size.width()
            item_new_h = custom_decoration_size.height()
        qsize = QSize(item_new_w, item_new_h)
        return qsize

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> None:
        with elapsed_timer() as elapsed:
            item_size = option.rect.size()
            custom_decoration_w, custom_decoration_h = index.data(SlideListModel.DecorationSizeOrRatioRole)
            if option.decorationPosition == QStyleOptionViewItem.Left:
                text_x, text_y = custom_decoration_w + self.icon_and_text_spacing, 0
                text_width = item_size.width() - custom_decoration_w - self.icon_and_text_spacing
                text_height = custom_decoration_h
            elif option.decorationPosition == QStyleOptionViewItem.Top:
                text_size = super().sizeHint(option, index)
                custom_decoration_h = custom_decoration_h - text_size.height()
                text_x, text_y = 0, custom_decoration_h + self.icon_and_text_spacing
                text_width = custom_decoration_w
                text_height = item_size.height() - custom_decoration_h - self.icon_and_text_spacing

            slide_view_params: SlideViewParams = index.data(SlideListModel.SlideViewParamsRole)
            scene_rect = QRectF(*slide_view_params.level_rect)
            img_key = "{}_{}_{}".format(custom_decoration_w, custom_decoration_h, slide_view_params.cache_key())
            icon_pixmap = QPixmapCache.find(img_key)
            if icon_pixmap is None:
                # print("read", img_key)
                scene = QGraphicsScene()
                t1 = elapsed()
                print("before slide_graphics", t1)
                slide_graphics = SlideGraphicsGroup(slide_view_params)
                t2 = elapsed()
                print("slide_graphics", t2 - t1)
                scene.clear()
                scene.invalidate()
                scene.addItem(slide_graphics)
                slide_graphics.update_visible_level(slide_view_params.level)
                slide_helper = SlideHelper(slide_view_params.slide_path)
                scene.setSceneRect(slide_helper.get_rect_for_level(slide_view_params.level))
                image = build_screenshot_image(scene, QSize(custom_decoration_w, custom_decoration_h), scene_rect)
                t3 = elapsed()
                print("build_screenshot_image", t3 - t2)
                icon_pixmap = QtGui.QPixmap.fromImage(image)
                QPixmapCache.insert(img_key, icon_pixmap)
            t4 = elapsed()
            painter.fillRect(option.rect, painter.background())
            painter.drawPixmap(option.rect.topLeft(), icon_pixmap)
            # painter.drawRect(option.rect)
            painter.drawRect(option.rect.topLeft().x(), option.rect.topLeft().y(), icon_pixmap.width(),
                             icon_pixmap.height())

            option.rect = option.rect.translated(text_x, text_y)
            option.rect.setSize(QSize(text_width, text_height))
            # print("rect:", option.rect)
            # t4 = elapsed()
            # if t3 is None:
            #     t3 = 0
            # t5 = elapsed()
            # print("finally", t5 - t4)
            super().paint(painter, option, index)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QtCore.QModelIndex) -> QWidget:
        # print(option.displayAlignment)
        # print(option.viewItemPosition)
        # print(option.decorationAlignment)
        # print(option.decorationPosition)
        slide_viewer_editor = SlideViewerEditor(parent, option.decorationPosition == QStyleOptionViewItem.Top)
        slide_viewer_editor.setGeometry(option.rect)
        return slide_viewer_editor

    def updateEditorGeometry(self, editor: SlideViewerEditor, option: QStyleOptionViewItem,
                             index: QtCore.QModelIndex) -> None:
        editor.layout().setContentsMargins(0, 0, 0, 0)
        editor.slide_viewer.layout().setContentsMargins(0, 0, 0, 0)
        super().updateEditorGeometry(editor, option, index)
