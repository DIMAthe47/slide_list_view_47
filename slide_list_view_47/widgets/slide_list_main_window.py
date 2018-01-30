from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QActionGroup, QGroupBox, QFormLayout, QHBoxLayout, \
    QLineEdit, QDialogButtonBox, QVBoxLayout, QDialog, QListView, QAction, QStyledItemDelegate

from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.model.role_funcs import item_func, slideviewparams_decoration_func, \
    decoration_size_func_factory
from slide_list_view_47.widgets.actions.on_change_mode_menu import OnChangeModeMenu
from slide_list_view_47.widgets.actions.on_icon_max_size_or_ratio_action import OnIconMaxSizeOrRatioAction
from slide_list_view_47.widgets.actions.on_load_items_action import OnLoadItemsAction
from slide_list_view_47.widgets.actions.on_get_selected_items_action import OnGetSelectedItemsDataAction
from slide_list_view_47.widgets.slide_list_widget import SlideListWidget
from slide_list_view_47.widgets.slide_viewer_delegate import SlideViewerDelegate


class SlideListMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Slide list')
        self.resize(500, 600)
        self.slide_list_widget = SlideListWidget()
        self.setCentralWidget(self.slide_list_widget)
        self._saved_delegate = None

        menu_bar = self.menuBar()

        load_action_menu = menu_bar.addMenu("load_actions")
        self.load_action = OnLoadItemsAction("load", menu_bar)
        self.load_action.set_list_model(self.slide_list_widget.list_model)
        load_action_menu.addAction(self.load_action)
        menu_bar.addMenu(load_action_menu)

        get_slide_list_data_action = OnGetSelectedItemsDataAction(menu_bar)
        get_slide_list_data_action.set_list_view(self.slide_list_widget.list_view)
        menu_bar.addAction(get_slide_list_data_action)

        view_actions_menu = menu_bar.addMenu("view_actions")
        icon_max_size_or_ratio_action = OnIconMaxSizeOrRatioAction(self.slide_list_widget, view_actions_menu)
        # icon_max_size_or_ratio_action.triggered.connect(self.on_icon_max_size_or_ratio_action)

        change_view_mode_action = view_actions_menu.addAction("change view_mode")
        change_view_mode_action.triggered.connect(self.on_change_view_mode)

        self.on_change_mode_menu = OnChangeModeMenu(view_actions_menu)
        self.on_change_mode_menu.set_slide_list_widget(self.slide_list_widget)

        # view_actions_menu.addAction(self.text_mode_action)
        # view_actions_menu.addAction(self.decoration_mode_action)
        # view_actions_menu.addAction(self.delegate_mode_action)

    def on_change_view_mode(self):
        if self.slide_list_widget.list_view.viewMode() == QListView.IconMode:
            self.slide_list_widget.list_view.setViewMode(QListView.ListMode)
        else:
            self.slide_list_widget.list_view.setViewMode(QListView.IconMode)
