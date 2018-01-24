import sys

from PyQt5.QtGui import QPixmapCache
from PyQt5.QtWidgets import QAbstractItemView
from media_objects_47.widgets.media_object_main_window import MediaObjectMainWindow
from media_objects_47.widgets.slide_viewer_delegate import SlideViewerDelegate
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from slide_viewer_47.common.slide_tile import SlideTile


def excepthook(excType, excValue, tracebackobj):
    print(excType, excValue, tracebackobj)


sys.excepthook = excepthook


def display_func(item: SlideTile):
    return item.slide_path


def main():
    app = QApplication(sys.argv)
    win = MediaObjectMainWindow()
    cache_size_in_kb = 300 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)
    filepathes = [
        r'C:\Users\DIMA\PycharmProjects\slide_cbir_47\downloads\images\19403.svs',
        # r'C:\Users\DIMA\Downloads\11096.svs'
    ]
    media_objects = [
        SlideTile(filepath, None, None) for filepath in filepathes
    ]

    win.media_objects_widget.list_model.update_media_objects(media_objects)
    win.media_objects_widget.list_model.update_role_func(Qt.DisplayRole, display_func)
    win.media_objects_widget.list_view.setEditTriggers(
        QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
    item_delegate = SlideViewerDelegate()
    win.media_objects_widget.list_view.setItemDelegate(item_delegate)
    win.media_objects_widget.list_view.setMouseTracking(True)
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
