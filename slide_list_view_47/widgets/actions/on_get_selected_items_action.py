from PyQt5.QtWidgets import QAction, QMessageBox, QMenu, QMenuBar

from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_viewer_47.common.qt.my_action import MyAction


def default_data_consumer(data):
    QMessageBox.information(None, "default_data_consumer", str(data))


class OnGetSelectedItemsDataAction(MyAction):
    def __init__(self, title, parent, list_view, data_consumer=default_data_consumer):
        super().__init__(title, parent, self.on_get_data_action)
        self.list_view = list_view
        self.data_consumer = data_consumer

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
