import sys

import os
from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import QAbstractItemView, QStyledItemDelegate

from media_objects_47.model.role_funcs import item_func
from media_objects_47.widgets.media_object_main_window import MediaObjectMainWindow
from media_objects_47.widgets.slide_viewer_delegate import SlideViewerDelegate
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from slide_viewer_47.common.slide_tile import SlideTile, SlideViewParams


def excepthook(excType, excValue, tracebackobj):
    print(excType, excValue, tracebackobj)


sys.excepthook = excepthook


def display_func(item: SlideViewParams):
    return item.slide_path


def filepath_to_slideviewparams(filepath):
    return SlideViewParams(filepath)


def main():
    app = QApplication(sys.argv)
    win = MediaObjectMainWindow()
    cache_size_in_kb = 700 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)

    dirpath = r'C:\Users\DIMA\Google Диск\Pictures\Mountains'
    filepathes = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]

    # filepathes = [
    #     r'C:\Users\DIMA\PycharmProjects\slide_cbir_47\downloads\images\19403.svs',
        # r'C:\Users\DIMA\Downloads\11096.svs'
    # ]

    media_objects = [filepath_to_slideviewparams(filepath) for filepath in filepathes]
    win.load_action.media_object_builder = filepath_to_slideviewparams
    win.media_objects_widget.list_model.update_media_objects(media_objects)
    win.media_objects_widget.list_model.update_role_func(Qt.DisplayRole, display_func)

    win.media_objects_widget.list_model.update_role_func(Qt.EditRole, item_func)
    item_delegate = SlideViewerDelegate()
    win.media_objects_widget.list_view.setItemDelegate(item_delegate)

    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
