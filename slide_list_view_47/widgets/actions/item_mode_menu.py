from typing import Callable

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction, QGroupBox, QHBoxLayout, QLineEdit, QFormLayout, QDialog, QDialogButtonBox, \
    QVBoxLayout, QMenu, QActionGroup, QStyledItemDelegate

from slide_list_view_47.model.role_funcs import decoration_size_func_factory, slideviewparams_to_pixmap, \
    slidepath_to_pximap, slideviewparams_to_str
from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.widgets.slide_list_widget import SlideListWidget
from slide_list_view_47.widgets.slide_viewer_delegate import SlideViewerDelegate
from slide_viewer_47.common.slide_view_params import SlideViewParams


class ItemModeMenu(QMenu):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.window = None
        if isinstance(parent, QMenu):
            self.window = parent.parent()
            parent.addMenu(self)

        self.slide_list_widget: SlideListWidget = None

        # by default items are slideviewparams
        self.item_to_pixmap = slideviewparams_to_pixmap
        self.item_to_str = slideviewparams_to_str
        self.item_to_slideviewparams = lambda x: x

        self.action_group = QActionGroup(self)
        self.text_mode_action = QAction("text", self.action_group)
        self.text_mode_action.setCheckable(True)
        self.text_mode_action.triggered.connect(self.on_text_mode_action)
        self.decoration_mode_action = QAction("text+decoration", self.action_group)
        self.decoration_mode_action.setCheckable(True)
        self.decoration_mode_action.triggered.connect(self.on_decoration_mode_action)
        self.delegate_mode_action = QAction("slide_viewer_delegate", self.action_group)
        self.delegate_mode_action.setCheckable(True)
        self.delegate_mode_action.triggered.connect(self.on_delegate_mode_action)

        self.addAction(self.text_mode_action)
        self.addAction(self.decoration_mode_action)
        self.addAction(self.delegate_mode_action)

    def set_slide_list_widget(self, slide_list_widget: SlideListWidget):
        self.slide_list_widget = slide_list_widget
        self.delegate_mode_action.trigger()

    def on_text_mode_action(self):
        self.slide_list_widget.list_view.setItemDelegate(QStyledItemDelegate())
        list_model = self.slide_list_widget.list_model
        list_model.beginResetModel()
        self.slide_list_widget.list_model.text_mode(self.item_to_str)
        list_model.endResetModel()

    def on_decoration_mode_action(self):
        self.slide_list_widget.list_view.setItemDelegate(QStyledItemDelegate())
        list_model = self.slide_list_widget.list_model
        list_model.beginResetModel()
        self.slide_list_widget.list_model.decoration_mode(self.item_to_str, self.item_to_pixmap)
        list_model.endResetModel()

    def on_delegate_mode_action(self):
        self.slide_list_widget.list_view.setItemDelegate(SlideViewerDelegate())
        list_model = self.slide_list_widget.list_model
        list_model.beginResetModel()
        self.slide_list_widget.list_model.slideviewparams_mode(self.item_to_str, self.item_to_slideviewparams)
        list_model.endResetModel()

