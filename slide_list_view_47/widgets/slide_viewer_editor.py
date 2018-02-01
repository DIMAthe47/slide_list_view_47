import copy

from PyQt5.QtCore import QRectF, pyqtProperty
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from slide_viewer_47.common.slide_view_params import SlideViewParams
from slide_viewer_47.widgets.slide_viewer import SlideViewer


class SlideViewerEditor(QWidget):

    @pyqtProperty(SlideViewParams, user=True)
    def slide_view_params(self) -> SlideViewParams:
        # slide_view_params = copy.deepcopy(self.slide_viewer.slide_view_params)
        slide_view_params = self.slide_viewer.slide_view_params
        return slide_view_params

    @slide_view_params.setter
    def slide_tile(self, value: SlideViewParams):
        # self._slide_view_params = copy.deepcopy(value)
        self._slide_view_params = value
        self.slide_viewer.load(self._slide_view_params)

    def __init__(self, parent: QWidget, viewer_top_else_left) -> None:
        super().__init__(parent)
        self._slide_view_params = None
        self.slide_viewer = SlideViewer(viewer_top_else_left=viewer_top_else_left)
        self.setAutoFillBackground(True)
        layout = QVBoxLayout()
        layout.addWidget(self.slide_viewer)
        self.setLayout(layout)
