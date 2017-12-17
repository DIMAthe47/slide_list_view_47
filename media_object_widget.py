from PyQt5.QtWidgets import QWidget, QVBoxLayout
from media_object_list_model import MediaObjectListModel
from media_object_list_view import MediaObjectListView


class MediaObjectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.list_model = MediaObjectListModel()
        self.list_view = MediaObjectListView(self, (100, 100), self.list_model.on_icon_size_changed)
        self.list_view.setModel(self.list_model)

        layout = QVBoxLayout()
        layout.addWidget(self.list_view)
        self.setLayout(layout)
