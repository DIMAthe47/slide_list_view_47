import collections
import copy

from PyQt5.QtCore import QRectF, pyqtProperty
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from elapsed_timer import elapsed_timer
from slide_viewer_47.common.level_builders import build_rects_and_colors_for_grid
from slide_viewer_47.common.slide_view_params import SlideViewParams
from slide_viewer_47.common.slide_helper import SlideHelper
from slide_viewer_47.widgets.slide_viewer import SlideViewer
from slide_viewer_47.widgets.slide_viewer_menu import to_json
from tiling_utils import slice_rect2


class SlideViewerEditor(QWidget):

    @pyqtProperty(SlideViewParams, user=True)
    def slide_view_params(self) -> SlideViewParams:
        with elapsed_timer() as elapsed:
            slide_view_params = copy.deepcopy(self.slide_viewer.slide_view_params)
            # slide_view_params = self.slide_viewer.slide_view_params
            # print(elapsed())
            return slide_view_params

        # print("from viewer:", to_json(slide_view_params))
        return slide_view_params

    @slide_view_params.setter
    def slide_tile(self, value: SlideViewParams):
        with elapsed_timer() as elapsed:
            # self._slide_view_params = value
            self._slide_view_params = copy.deepcopy(value)
            # print(elapsed())

            slide_helper = SlideHelper(value.slide_path)
            # grid for testing purpose
            rects, colors = build_rects_and_colors_for_grid((224, 224), slide_helper.get_level_size(0),
                                                            slice_func=slice_rect2)
            # print(elapsed())
            self._slide_view_params.grid_rects_0_level = rects
            self._slide_view_params.grid_colors_0_level = colors
            # print("to viewer:", to_json(self._slide_view_params))
            self.slide_viewer.load(self._slide_view_params)

    def __init__(self, parent: QWidget, viewer_top_else_left) -> None:
        super().__init__(parent)
        self._slide_view_params = None
        self.slide_viewer = SlideViewer(viewer_top_else_left=viewer_top_else_left)
        self.setAutoFillBackground(True)
        layout = QVBoxLayout()
        layout.addWidget(self.slide_viewer)
        self.setLayout(layout)
