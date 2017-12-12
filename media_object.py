import sys

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListView, QAbstractItemView, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, \
    QApplication, QWidget, QAction, QMenu, QMessageBox


class MediaObject(object):
    def __init__(self, text, pilimg, data):
        self.text = text
        self.pilimg = pilimg
        self.data = data


class MediaObjectListModel(QAbstractListModel):
    def __init__(self, media_objects, img_size=(75, 75)):
        super().__init__()
        self.media_objects = media_objects
        self.img_size = img_size

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
                w, h = self.img_size
                pixmap = pixmap.scaled(w, h)
                return QVariant(pixmap)
        elif role == Qt.UserRole:
            return QVariant(self.media_objects[index.row()].data)
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
    return MediaObject(filepath, None, "default data")


def imagefilepath_to_media_object(filepath):
    pilimg = Image.open(filepath)
    return MediaObject(filepath, pilimg, "default data")


def default_data_consumer(data):
    QMessageBox.information(None, "default_data_consumer", str(data))


class OnLoadMediaObjectsAction(QAction):
    def __init__(self, parent, title="load"):
        super().__init__(title, parent)
        self.triggered.connect(self.on_load_action)
        self.list_view = None
        self.filepath_to_media_object_func = default_media_object_extractor
        self.parent = parent

    def set_media_object_extractor(self, media_object_extractor):
        self.filepath_to_media_object_func = media_object_extractor

    def set_list_view(self, list_view):
        self.list_view = list_view

    def on_load_action(self):
        filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files", "")
        self.update_media_objects(filepathes)

    def update_media_objects(self, filepathes):
        media_objects = [self.filepath_to_media_object_func(filepath) for filepath in filepathes]
        list_model = MediaObjectListModel(media_objects)
        self.list_view.setModel(list_model)


class OnGetDataSelectedMediaObjectsAction(QAction):
    def __init__(self, parent, title="get_data"):
        super().__init__(title, parent)
        self.triggered.connect(self.on_get_data_action)
        self.list_view = None
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


class MediaObjectMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Media objects')
        self.setMinimumSize(500, 600)
        media_objects_widget = MediaObjectWidget()
        self.setCentralWidget(media_objects_widget)
        menuBar = self.menuBar()

        loadFilepathMediaObjectsAction = OnLoadMediaObjectsAction(menuBar, "filepath only")
        loadFilepathMediaObjectsAction.set_list_view(media_objects_widget.list_view)

        loadImageMediaObjectsAction = OnLoadMediaObjectsAction(menuBar, "filepath plus image")
        loadImageMediaObjectsAction.set_list_view(media_objects_widget.list_view)
        loadImageMediaObjectsAction.set_media_object_extractor(imagefilepath_to_media_object)

        getDataMediaObjectsAction = OnGetDataSelectedMediaObjectsAction(menuBar)
        getDataMediaObjectsAction.set_list_view(media_objects_widget.list_view)

        menuBar.addAction(loadFilepathMediaObjectsAction)
        menuBar.addAction(loadImageMediaObjectsAction)
        menuBar.addAction(getDataMediaObjectsAction)


def main():
    app = QApplication(sys.argv)
    win = MediaObjectMainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
