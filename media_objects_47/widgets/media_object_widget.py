from PyQt5.QtWidgets import QWidget, QVBoxLayout

from media_objects_47.model.media_object_list_model import MediaObjectListModel
from media_objects_47.widgets.media_object_list_view import MediaObjectListView


class MediaObjectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.list_model = MediaObjectListModel()
        self.list_view = MediaObjectListView(self)
        self.list_view.setModel(self.list_model)

        layout = QVBoxLayout()
        layout.addWidget(self.list_view)
        self.setLayout(layout)
