import sys

import os
from PyQt5.QtGui import QPixmapCache

from slide_list_view_47.model.role_funcs import filepath_to_slideviewparams
from slide_list_view_47.widgets.slide_list_main_window import SlideListMainWindow
from PyQt5.QtWidgets import QApplication


def excepthook(excType, excValue, tracebackobj):
    print(excType, excValue, tracebackobj)


sys.excepthook = excepthook


def main():
    app = QApplication(sys.argv)
    win = SlideListMainWindow()
    cache_size_in_kb = 700 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)

    # dirpath = r'C:\Users\DIMA\Google Диск\Pictures\Mountains'
    dirpath = r'C:\Users\DIMA\Downloads\svs'
    filepathes = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
    items = [filepath_to_slideviewparams(filepath) for filepath in filepathes]
    win.slide_list_widget.list_model.update_items(items)

    win.delegate_mode_action.trigger()

    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
