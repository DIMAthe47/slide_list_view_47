from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QListView, QAbstractItemView


class MediaObjectListView(QListView):
    wheelEventSignal = pyqtSignal(QtGui.QWheelEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setViewMode(QtWidgets.QListView.ListMode)
        self.setSpacing(2)
        self.setUniformItemSizes(True)
        self.setWordWrap(True)

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        self.wheelEventSignal.emit(e)
        super().wheelEvent(e)
