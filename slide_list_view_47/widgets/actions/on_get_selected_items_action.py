from PyQt5.QtWidgets import QAction, QMessageBox

from slide_list_view_47.model.slide_list_model import SlideListModel


class OnGetSelectedItemsDataAction(QAction):
    def __init__(self, parent, title="get_selected_items"):
        super().__init__(title, parent)
        self.triggered.connect(self.on_get_data_action)
        self.list_model = None
        self.data_consumer = default_data_consumer
        self.parent = parent

    def set_data_consumer(self, data_consumer):
        self.data_consumer = data_consumer

    def set_list_view(self, list_view):
        self.list_view = list_view

    def on_get_data_action(self):
        data = []
        for index in self.list_view.selectionModel().selectedIndexes():
            selected_media_object_data = self.list_view.model().data(index, SlideListModel.ItemRole).value()
            data.append(selected_media_object_data)
        self.data_consumer(data)


def default_data_consumer(data):
    QMessageBox.information(None, "default_data_consumer", str(data))