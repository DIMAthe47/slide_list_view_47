import random
import sys

import math
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QSize, QRectF, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPen
from PyQt5.QtWidgets import QListView, QAbstractItemView, QMainWindow, QVBoxLayout, QFileDialog, \
    QApplication, QWidget, QAction, QMessageBox, QActionGroup
import itertools

from math import ceil


class MediaObject(object):
    def __init__(self, text, pilimg_or_pixmap, data):
        self.text = text
        self.pilimg_or_pixmap = pilimg_or_pixmap
        self.data = data


class PixmapWithMaskedTiles(QPixmap):
    def __init__(self, pilimg_or_path, tile_rects, qcolors: list) -> None:
        img = ImageQt(pilimg_or_path)
        pixmap = QtGui.QPixmap.fromImage(img)
        self.original_pixmap = pixmap
        super().__init__(pixmap)
        # self.load(img)
        self.tile_rects = tile_rects
        self.fill(QColor(0, 0, 0, 255))
        self.qcolors = qcolors
        self.mask_on()

    def mask_on(self):
        painter = QPainter(self)
        painter.save()
        painter.drawPixmap(self.rect(), self.original_pixmap)
        for i, tile_rect in enumerate(self.tile_rects):
            # print("last tile_rect", tile_rect)
            pen = QPen(QColor(0, 0, 0, 255))
            brush = QBrush(self.qcolors[i])
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect(QRectF(*tile_rect))
            qcolor = self.qcolors[i]
            # painter.drawText(QRect(*tile_rect), Qt.AlignCenter, str(qcolor.alpha()))
            # painter.drawText(QRect(*tile_rect), Qt.AlignBottom, str(i))

            # painter.fillRect(*tile_rect, self.qcolors[i])
        painter.restore()
        painter.end()

    def mask_off(self):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.original_pixmap, self.rect())
        painter.end()


class MediaObjectListModel(QAbstractListModel):
    def __init__(self, media_objects, icon_size):
        super().__init__()
        self.media_objects = media_objects
        self.icon_size = icon_size

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
            pilimg_or_pixmap = self.media_objects[index.row()].pilimg_or_pixmap
            if pilimg_or_pixmap:
                if not isinstance(pilimg_or_pixmap, QPixmap):
                    img = ImageQt(pilimg_or_pixmap)
                    pixmap = QtGui.QPixmap.fromImage(img)
                else:
                    pixmap = pilimg_or_pixmap
                w, h = self.icon_size
                pixmap = pixmap.scaled(w, h)
                print(pixmap.size())
                return QVariant(pixmap)
        elif role == Qt.UserRole:
            return QVariant(self.media_objects[index.row()].data)
        else:
            return QVariant()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


class MediaObjectListView(QListView):
    def __init__(self, parent=None, media_objects_per_viewport=3):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setViewMode(QtWidgets.QListView.ListMode)
        # self.setGridSize(QSize(75, 75))
        self.setSpacing(2)
        self.media_objects_per_viewport = media_objects_per_viewport
        self.update_media_objects_per_viewport(media_objects_per_viewport)

    def update_media_objects_per_viewport(self, media_objects_per_viewport):
        self.media_objects_per_viewport = media_objects_per_viewport
        view_size = self.viewport().size()
        icon_height = view_size.height() // self.media_objects_per_viewport - self.spacing() * 2
        self.icon_size = (icon_height, icon_height)

    def update_media_objects(self, media_objects):
        self.update_media_objects_per_viewport(self.media_objects_per_viewport)
        list_model = MediaObjectListModel(media_objects, icon_size=self.icon_size)
        self.setModel(list_model)


class MediaObjectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.list_view = MediaObjectListView()
        self.list_model = MediaObjectListModel([], self.list_view.icon_size)
        self.list_view.setModel(self.list_model)
        layout = QVBoxLayout()
        layout.addWidget(self.list_view)
        self.setLayout(layout)


def default_media_object_extractor(source):
    return MediaObject(source, None, "default data")


def imagefilepath_to_media_object(filepath):
    pilimg = Image.open(filepath)
    return MediaObject(filepath, pilimg, "default data")


def chop(length, n_chops):
    regular_chop_length = math.ceil(length / n_chops)
    chops = [regular_chop_length * i for i in range(n_chops)]
    offsets = [min((length - i * regular_chop_length, regular_chop_length)) for i in range(n_chops)]
    return chops, offsets


def repeat_each_n_times(iterable, n):
    repeated_iter = zip(*[iter(iterable) for i in range(n)])
    return itertools.chain.from_iterable(repeated_iter)


def tile_rect(width, height, columns, rows):
    x_poses, widths = chop(width, columns)
    y_poses, heights = chop(height, rows)
    x_iter = itertools.cycle(x_poses)
    width_iter = itertools.cycle(widths)
    y_iter = repeat_each_n_times(y_poses, columns)
    height_iter = repeat_each_n_times(heights, columns)
    tiles_rects = list(zip(x_iter, y_iter, width_iter, height_iter))
    return tiles_rects


def chess_positions(columns, rows):
    return [(i, j) for i in range(rows) for j in range(columns) if (i + j) % 2 != 0]


def random_qcolor(alpha):
    return QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)


def imagefilepath_to_media_object_with_masked_tiles(filepath):
    pilimg = Image.open(filepath)
    columns, rows = 7, 7
    masked_tile_rects = tile_rect(pilimg.width, pilimg.height, columns, rows)
    chess_positions_ = chess_positions(columns, rows)
    chess_tile_rects = [masked_tile_rects[i * columns + j] for i in range(rows) for j in range(columns) if
                        (i, j) in chess_positions_]
    # qcolors = [random_qcolor(128) for i in range(columns * rows)]
    qcolors = [QColor(0, 255, 0, 128) for i in range(columns * rows)]
    pixmap = PixmapWithMaskedTiles(filepath, chess_tile_rects, qcolors)
    return MediaObject(filepath, pixmap, "default data")


def imagefilepath_to_media_object_with_pixmap(filepath):
    pixmap = QPixmap(filepath)
    return MediaObject(filepath, pixmap, "default data")


def default_data_consumer(data):
    QMessageBox.information(None, "default_data_consumer", str(data))


media_object_extractors = {
    "filepath": default_media_object_extractor,
    "filepath+pilimg": imagefilepath_to_media_object,
    "filepath+pixmap": imagefilepath_to_media_object_with_pixmap,
    "filepath+masked_tiles_pixmap": imagefilepath_to_media_object_with_masked_tiles,
}


class OnLoadMediaObjectsAction(QAction):
    def __init__(self, parent, title="load"):
        super().__init__(title, parent)
        self.triggered.connect(self.on_load_action)
        self.list_view = None
        self.media_object_extractor = default_media_object_extractor
        self.parent = parent

    def set_media_object_extractor(self, media_object_extractor):
        self.media_object_extractor = media_object_extractor

    def set_list_view(self, list_view):
        self.list_view = list_view

    def on_load_action(self):
        # filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files", "")
        filepathes, _ = QFileDialog.getOpenFileNames(self.parent, "Choose files",
                                                     "/home/dimathe47/data/geo_tiny/Segm_RemoteSensing1/cropped")
        self.update_list_view(filepathes)

    def update_list_view(self, filepathes):
        media_objects = [self.media_object_extractor(source) for source in filepathes]
        self.list_view.update_media_objects(media_objects)


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
        # media_objects_widget.list_view.setViewMode(QtWidgets.QListView.IconMode)

        self.media_objects_widget = media_objects_widget
        self.setCentralWidget(media_objects_widget)
        menuBar = self.menuBar()

        load_action_menu = menuBar.addMenu("load")
        load_action_group = QActionGroup(load_action_menu)
        self.load_actions = {}
        for media_object_extractor_title in media_object_extractors:
            action = OnLoadMediaObjectsAction(load_action_menu, media_object_extractor_title)
            action.setCheckable(True)
            action.set_list_view(media_objects_widget.list_view)
            action.set_media_object_extractor(media_object_extractors[media_object_extractor_title])
            load_action_group.addAction(action)
            load_action_menu.addAction(action)
            self.load_actions[media_object_extractor_title] = action

        getDataMediaObjectsAction = OnGetDataSelectedMediaObjectsAction(menuBar)
        getDataMediaObjectsAction.set_list_view(media_objects_widget.list_view)
        menuBar.addAction(getDataMediaObjectsAction)


def main():
    app = QApplication(sys.argv)
    win = MediaObjectMainWindow()
    win.show()

    default_action = win.load_actions["filepath+masked_tiles_pixmap"]
    filepathes = [
                     '/home/dimathe47/data/geo_tiny/Segm_RemoteSensing1/cropped/poligon_minsk_1_yandex_z18_train_0_0.jpg'] * 10
    default_action.update_list_view(filepathes)
    default_action.setChecked(True)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
