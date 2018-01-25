import collections

from PyQt5.QtCore import QRectF, pyqtProperty
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from slide_viewer_47.common.slide_tile import SlideTile
from slide_viewer_47.widgets.slide_viewer import SlideViewer


class SlideViewerEditor(QWidget):

    @pyqtProperty(SlideTile, user=True)
    def slide_tile(self) -> SlideTile:
        # downsample = self.slide_viewer.slide_helper.get_downsample_for_level(self.slide_viewer.current_level)
        # level = slide_helper.get_best_level_for_downsample(downsample)
        slide_tile = SlideTile(self._slide_tile.slide_path, self.slide_viewer.current_level,
                               self.slide_viewer.get_current_view_scene_rect())
        print("from viewer:", self.slide_viewer.current_level, self.slide_viewer.get_current_view_scene_rect())
        return slide_tile

    @slide_tile.setter
    def slide_tile(self, value: SlideTile):
        self._slide_tile = value
        start_level, start_rect = None, None
        if value.level is not None and value.rect is not None:
            start_level = value.level
            if isinstance(value.rect, collections.Iterable):
                start_rect = QRectF(*value.rect)
            else:
                start_rect = value.rect

        print("to viewer:", start_level, start_rect)
        self.slide_viewer.load_slide(value.slide_path, start_level, start_rect)

    def __init__(self, parent: QWidget, viewer_top_else_left) -> None:
        super().__init__(parent)
        self._slide_tile = None
        self.slide_viewer = SlideViewer(viewer_top_else_left=viewer_top_else_left)
        self.setAutoFillBackground(True)
        layout = QVBoxLayout()
        # layout.addWidget(QTextEdit("123123"))
        layout.addWidget(self.slide_viewer)
        self.setLayout(layout)
