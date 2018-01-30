from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QActionGroup, QGroupBox, QFormLayout, QHBoxLayout, \
    QLineEdit, QDialogButtonBox, QVBoxLayout, QDialog, QListView, QAction, QStyledItemDelegate

from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.model.role_funcs import item_func, slideviewparams_decoration_func, \
    decoration_size_func_factory
from slide_list_view_47.widgets.actions.list_view_mode_menu import ListViewModeMenu
from slide_list_view_47.widgets.actions.item_mode_menu import ItemModeMenu
from slide_list_view_47.widgets.actions.on_change_view_mode_action import OnChangeViewModeAction
from slide_list_view_47.widgets.actions.on_icon_max_size_or_ratio_action import OnIconMaxSizeOrRatioAction
from slide_list_view_47.widgets.actions.on_load_items_action import OnLoadItemsAction
from slide_list_view_47.widgets.actions.on_get_selected_items_action import OnGetSelectedItemsDataAction
from slide_list_view_47.widgets.slide_list_widget import SlideListWidget
from slide_list_view_47.widgets.slide_viewer_delegate import SlideViewerDelegate


class SlideListMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('slide_list_view_47')
        self.resize(500, 600)
        self.slide_list_widget = SlideListWidget()
        self.setCentralWidget(self.slide_list_widget)
        self._saved_delegate = None

        menu_bar = self.menuBar()

        load_action_menu = menu_bar.addMenu("load_actions")
        self.load_action = OnLoadItemsAction("load", load_action_menu)
        self.load_action.set_list_model(self.slide_list_widget.list_model)
        menu_bar.addMenu(load_action_menu)

        get_slide_list_data_action = OnGetSelectedItemsDataAction("get_selected_items", menu_bar)
        get_slide_list_data_action.set_list_view(self.slide_list_widget.list_view)

        list_view_menu = ListViewModeMenu("list_view", menu_bar)
        list_view_menu.set_slide_list_widget(self.slide_list_widget)
