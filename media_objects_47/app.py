import sys

import os
from PyQt5.QtGui import QPixmapCache

from media_objects_47.model.role_funcs import item_func, slideviewparams_to_str, filepath_to_slideviewparams
from media_objects_47.widgets.media_object_main_window import MediaObjectMainWindow
from media_objects_47.widgets.slide_viewer_delegate import SlideViewerDelegate
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


def excepthook(excType, excValue, tracebackobj):
    print(excType, excValue, tracebackobj)


sys.excepthook = excepthook


def main():
    app = QApplication(sys.argv)
    win = MediaObjectMainWindow()
    cache_size_in_kb = 700 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)

    # dirpath = r'C:\Users\DIMA\Google Диск\Pictures\Mountains'
    # filepathes = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
    # filepathes = [
    #     r'C:\Users\DIMA\PycharmProjects\slide_cbir_47\downloads\images\19403.svs',
        # r'C:\Users\DIMA\Downloads\11096.svs'
    # ]
    # media_objects = [filepath_to_slideviewparams(filepath) for filepath in filepathes]
    # win.media_objects_widget.list_model.update_media_objects(media_objects)

    win.delegate_mode_action.trigger()

    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
