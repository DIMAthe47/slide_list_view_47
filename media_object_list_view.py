from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QListView, QAbstractItemView
from media_object_list_model import MediaObjectListModel


# Note that MediaObjectListView view doesnt know about MediaObjectListModel
class MediaObjectListView(QListView):
    def __init__(self, parent=None, icon_max_size_or_ratio=(0.2, 0.25),
                 icon_size_changed_callback=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setViewMode(QtWidgets.QListView.ListMode)
        # self.setGridSize(QSize(75, 75))
        self.setSpacing(2)
        self.icon_max_size_or_ratio = icon_max_size_or_ratio
        self.icon_size_changed_callback = icon_size_changed_callback
        self.update_icon_size()

    def update_icon_max_size_or_ratio(self, icon_max_size_or_ratio):
        self.icon_max_size_or_ratio = icon_max_size_or_ratio
        self.update_icon_size()

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        super().resizeEvent(e)
        self.update_icon_size()

    def update_icon_size(self):
        view_size = self.viewport().size()

        if isinstance(self.icon_max_size_or_ratio[1], float):
            icon_height = view_size.height() * self.icon_max_size_or_ratio[1] - self.spacing() * 2
        else:
            icon_height = self.icon_max_size_or_ratio[1]

        if isinstance(self.icon_max_size_or_ratio[0], float):
            icon_width = view_size.width() * self.icon_max_size_or_ratio[0] - self.spacing() * 2
        else:
            icon_width = self.icon_max_size_or_ratio[0]

        self.icon_size = (icon_width, icon_height)
        if self.icon_size_changed_callback:
            self.icon_size_changed_callback(self.icon_size)
