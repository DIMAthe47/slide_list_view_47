from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QFileDialog
from media_object import default_media_object_extractor, default_data_consumer


class OnLoadMediaObjectsAction(QAction):
    def __init__(self, parent, title="load"):
        super().__init__(title, parent)
        self.triggered.connect(self.on_load_action)
        self.list_model = None
        self.media_object_extractor = default_media_object_extractor
        self.parent = parent

    def set_media_object_extractor(self, media_object_extractor):
        self.media_object_extractor = media_object_extractor

    def set_list_model(self, list_model):
        self.list_model = list_model

    def on_load_action(self):
        # filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files", "")
        filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files",
                                                     "/home/dimathe47/data/geo_tiny/Segm_RemoteSensing1/cropped")
        self.update_list_model(filepathes)

    def update_list_model(self, filepathes):
        media_objects = [self.media_object_extractor(source) for source in filepathes]
        self.list_model.update_media_objects(media_objects)


class OnGetSelectedMediaObjectsDataAction(QAction):
    def __init__(self, parent, title="get_data"):
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
            selected_media_object_data = self.list_view.model().data(index, Qt.UserRole).value()
            data.append(selected_media_object_data)
        self.data_consumer(data)
