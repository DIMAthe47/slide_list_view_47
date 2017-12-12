import sys
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant
from PyQt5.QtWidgets import QListView, QAbstractItemView, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, \
    QApplication, QWidget, QAction, QMenu


class MediaObject(object):
    def __init__(self, text, pilimg, data):
        self.text = text
        self.pilimg = pilimg
        self.data = data


class MediaObjectListModel(QAbstractListModel):
    def __init__(self, media_objects):
        super().__init__()
        self.media_objects = media_objects

    def rowCount(self, parent=QModelIndex()):
        return len(self.media_objects)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return QVariant(self.media_objects[index.row()].text)
        elif role == Qt.EditRole:
            return QVariant(self.media_objects[index.row()].text)
        elif role == Qt.ToolTipRole:
            return QVariant(self.media_objects[index.row()].text)
        elif role == Qt.DecorationRole:
            pilimg = self.media_objects[index.row()].pilimg
            if pilimg:
                qim = ImageQt(pilimg)
                pixmap = QtGui.QPixmap.fromImage(qim)
                w = 100
                h = 100
                pixmap = pixmap.scaled(w, h)
                return QVariant(pixmap)
        else:
            return QVariant()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


class MediaObjectListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)


class MediaObjectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.list_view = MediaObjectListView()
        self.list_model = MediaObjectListModel([])
        self.list_view.setModel(self.list_model)
        layout = QVBoxLayout()
        layout.addWidget(self.list_view)
        self.setLayout(layout)


def default_media_object_extractor(filepath):
    return MediaObject(filepath, None, None)


class OnLoadMediaObjectsAction(QAction):
    def __init__(self, parent, title="load"):
        super().__init__(title, parent)
        self.triggered.connect(self.on_load_action)
        self.list_model = None
        self.media_object_extractor = default_media_object_extractor
        self.parent = parent

    def set_media_object_extractor(self, media_object_extractor):
        self.media_object_extractor = media_object_extractor

    def set_list_view(self, list_view):
        self.list_view = list_view

    def on_load_action(self):
        filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files", "")
        self.update_media_objects(filepathes)

    def update_media_objects(self, filepathes):
        media_objects = [self.media_object_extractor(filepath) for filepath in filepathes]
        list_model = MediaObjectListModel(media_objects)
        self.list_view.setModel(list_model)


class MediaObjectsMenu(QMenu):
    def __init__(self, parent, title="media objects"):
        super().__init__(title, parent)
        self.load_action = QAction("load", parent)
        # self.loadAction = QAction("clear", parent)
        self.addAction(self.load_action)
        self.load_action.triggered.connect(self.on_load_action)
        self.list_model = None
        self.media_object_extractor = default_media_object_extractor
        self.parent = parent

    def set_media_object_extractor(self, media_object_extractor):
        self.media_object_extractor = media_object_extractor

    def set_list_view(self, list_view):
        self.list_view = list_view

    def on_load_action(self):
        filepathes, _ = QFileDialog.getOpenFileNames(self, "Choose files", "")
        self.update_media_objects(filepathes)

    def update_media_objects(self, filepathes):
        media_objects = [self.media_object_extractor(filepath) for filepath in filepathes]
        list_model = MediaObjectListModel(media_objects)
        self.list_view.setModel(list_model)


class MediaObjectMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Image List')
        self.setMinimumSize(500, 600)
        layout = QVBoxLayout()
        media_objects_widget = MediaObjectWidget()
        self.setCentralWidget(media_objects_widget)

        menuBar = self.menuBar()
        loadMediaObjectsAction = OnLoadMediaObjectsAction(menuBar)
        loadMediaObjectsAction.set_list_view(media_objects_widget.list_view)
        menuBar.addAction(loadMediaObjectsAction)

        # menu = MediaObjectsMenu(menuBar)
        # menu.set_list_view(media_objects_widget.list_view)
        # menuBar.addMenu(menu)

        # img_dir = '/home/dimathe47/data/geo_tiny/Segm_RemoteSensing1/cropped'
        # import os
        # img_names = os.listdir(img_dir)
        #
        # pilimg_text_list = [{"idx": i, "pilimg": Image.open(os.path.join(img_dir, img_name)), "text": img_name} for
        #                     i, img_name in
        #                     enumerate(img_names)]
        # image_list_model = ImageTextListModel(pilimg_text_list)
        # self.list_view.setModel(image_list_model)


def main():
    app = QApplication(sys.argv)
    win = MediaObjectMainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
