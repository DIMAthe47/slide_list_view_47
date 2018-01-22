from PyQt5.QtWidgets import QAction, QFileDialog


class OnLoadMediaObjectsAction(QAction):
    def __init__(self, title="load", parent=None):
        super().__init__(title, parent)
        self.triggered.connect(self.on_load_action)
        self.list_model = None
        self.parent = parent

    def set_list_model(self, list_model):
        self.list_model = list_model

    def on_load_action(self):
        filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files", "")
        # filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files",
        #                                              "/home/dimathe47/data/geo_tiny/Segm_RemoteSensing1/cropped")
        if filepathes and len(filepathes) > 0:
            self.update_list_model(filepathes)

    def update_list_model(self, filepathes):
        self.list_model.update_media_objects(filepathes)
