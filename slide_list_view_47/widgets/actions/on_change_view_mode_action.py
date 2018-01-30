from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QAction, QGroupBox, QHBoxLayout, QLineEdit, QFormLayout, QDialog, QDialogButtonBox, \
    QVBoxLayout, QMenu, QListView

from slide_list_view_47.model.role_funcs import decoration_size_func_factory
from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.widgets.slide_list_widget import SlideListWidget


class OnChangeViewModeAction(QAction):
    def __init__(self, title, parent, list_view):
        super().__init__(title, parent)
        self.window = None
        if isinstance(parent, QMenu):
            self.window = parent.parent()
            parent.addAction(self)
        self.triggered.connect(self.on_action)
        self.list_view = list_view

    def on_action(self):
        if self.list_view.viewMode() == QListView.IconMode:
            self.list_view.setViewMode(QListView.ListMode)
        else:
            self.list_view.setViewMode(QListView.IconMode)
