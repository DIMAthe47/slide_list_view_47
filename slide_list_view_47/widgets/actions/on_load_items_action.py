from PyQt5.QtWidgets import QAction, QFileDialog, QMenu, QMenuBar

from slide_list_view_47.model.role_funcs import slidepath_to_slideviewparams
from slide_viewer_47.common.qt.my_action import MyAction


class OnLoadItemsAction(MyAction):
    def __init__(self, title, parent, list_model, media_object_builder=slidepath_to_slideviewparams):
        super().__init__(title, parent, self.on_load_action)
        self.list_model = list_model
        self.media_object_builder = media_object_builder

    def on_load_action(self):
        filepathes, _ = QFileDialog.getOpenFileNames(self.window, "Choose files", "")
        # filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files",
        #                                              "/home/dimathe47/data/geo_tiny/Segm_RemoteSensing1/cropped")
        if filepathes and len(filepathes) > 0:
            self.update_list_model(filepathes)

    def update_list_model(self, filepathes):
        mediaobjects = [self.media_object_builder(filepath) for filepath in filepathes]
        self.list_model.update_items(mediaobjects)
