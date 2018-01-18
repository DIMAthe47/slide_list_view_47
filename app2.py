import sys
from PyQt5 import QtCore

from PyQt5.QtGui import QPixmapCache, QPainter, QColor, QRegion
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QVariant
from PyQt5.QtWidgets import QApplication, QItemDelegate, QStyleOptionViewItem, QWidget
from media_object_main_window import MediaObjectMainWindow
import os

from slide_viewer import SlideViewer


class SlideViewerDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)
        self.slide_path__slide_viewer = {}

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        saved_device = painter.device()

        # self.initStyleOption(option, index)
        slide_viewer = self.get_slideviewer(index)

        mappedorigin = painter.deviceTransform().map(option.rect.topLeft())
        painter.end()
        slide_viewer.render(painter.device(), mappedorigin, flags=QWidget.DrawChildren)

        # if pixmap:
        #     painter.fillRect(option.rect, QColor(255, 0, 0))

        # mappedorigin = painter.deviceTransform().map(option.rect.topLeft())
        # painter.end()
        # self.mw.render(painter.device(), mappedorigin, QRegion(self.mw.rect()), flags=QWidget.DrawChildren)

        painter.begin(saved_device)
        # QStyledItemDelegate.paint(self, painter, option, index)

    def editorEvent(self, event: QtCore.QEvent, model: QtCore.QAbstractItemModel, option: 'QStyleOptionViewItem',
                    index: QtCore.QModelIndex) -> bool:
        slide_viewer = self.get_slideviewer(index)
        return QApplication.instance().sendEvent(slide_viewer, event)
        # return super().editorEvent(event, model, option, index)

    def sizeHint(self, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QtCore.QSize:
        return self.get_slideviewer(index).size()

    def get_slideviewer(self, index):
        filepath = index.data(Qt.DisplayRole)
        if filepath in self.slide_path__slide_viewer:
            slide_viewer = self.slide_path__slide_viewer[filepath]
        else:
            slide_viewer = SlideViewer(self.parent)
            slide_viewer.load_slide(filepath)
            self.slide_path__slide_viewer[filepath] = slide_viewer
        return slide_viewer



def excepthook(excType, excValue, tracebackobj):
    print(excType, excValue, tracebackobj)


sys.excepthook = excepthook


def main():
    app = QApplication(sys.argv)
    win = MediaObjectMainWindow()
    cache_size_in_kb = 300 * 10 ** 3
    QPixmapCache.setCacheLimit(cache_size_in_kb)

    slideViewerDelegate = SlideViewerDelegate()
    win.media_objects_widget.list_view.setItemDelegate(slideViewerDelegate)
    win.media_objects_widget.list_view.setMouseTracking(True)
    win.show()

    default_action = win.load_actions[list(win.load_actions.keys())[0]]
    # filepathes = [
    #                  '/home/dimathe47/data/geo_tiny/Segm_RemoteSensing1/jpg-png/poligon_minsk_1_yandex_z18_train_0_0.jpg',
    #                  '/home/dimathe47/data/geo_tiny/Segm_RemoteSensing1/jpg-png/poligon_minsk_1_yandex_z18_train_0_0.png'] * 4
    # dirpath = '/home/dimathe47/Downloads/Mountains'
    # dirpath = r'C:\Users\DIMA\Google Диск\Pictures\Mountains'
    # filepathes = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]
    filepathes = [
        r'C:\Users\DIMA\Downloads\11096.svs'
    ]
    default_action.update_list_model(filepathes)
    default_action.setChecked(True)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
