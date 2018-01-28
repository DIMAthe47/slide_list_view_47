from PyQt5.QtWidgets import QWidget, QVBoxLayout

from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.widgets.slide_list_view import SlideListView


class SlideListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAcceptDrops(True)

        self.list_model = SlideListModel()
        self.list_view = SlideListView(self)
        self.list_view.setModel(self.list_model)

        layout = QVBoxLayout()
        layout.addWidget(self.list_view)
        self.setLayout(layout)
