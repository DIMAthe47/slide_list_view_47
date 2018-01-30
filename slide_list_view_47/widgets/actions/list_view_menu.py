from typing import Callable

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction, QGroupBox, QHBoxLayout, QLineEdit, QFormLayout, QDialog, QDialogButtonBox, \
    QVBoxLayout, QMenu, QActionGroup, QStyledItemDelegate, QMenuBar

from slide_list_view_47.widgets.actions.item_mode_menu import ItemModeMenu
from slide_list_view_47.widgets.actions.on_change_view_mode_action import OnChangeViewModeAction
from slide_list_view_47.widgets.actions.on_icon_max_size_or_ratio_action import OnIconMaxSizeOrRatioAction
from slide_list_view_47.widgets.slide_list_widget import SlideListWidget


class ListViewMenu(QMenu):
    def __init__(self, title, parent, slide_list_widget: SlideListWidget):
        super().__init__(title, parent)
        self.window = None
        if isinstance(parent, QMenu) or isinstance(parent, QMenuBar):
            self.window = parent.parent()
            parent.addMenu(self)

        self.slide_list_widget = slide_list_widget
        self.clear()
        icon_max_size_or_ratio_action = OnIconMaxSizeOrRatioAction("change icon_size_or_ratio", self,
                                                                   self.slide_list_widget)
        change_view_mode_action = OnChangeViewModeAction("change view mode", self, self.slide_list_widget.list_view)

        self.item_mode_menu = ItemModeMenu("change mode", self, self.slide_list_widget)
