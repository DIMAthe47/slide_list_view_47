from PyQt5.QtWidgets import QMainWindow

from slide_list_view_47.widgets.actions.list_view_menu import ListViewMenu
from slide_list_view_47.widgets.actions.on_load_items_action import OnLoadItemsAction
from slide_list_view_47.widgets.actions.on_get_selected_items_action import OnGetSelectedItemsDataAction
from slide_list_view_47.widgets.slide_list_widget import SlideListWidget


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
        self.load_action = OnLoadItemsAction("load", load_action_menu, self.slide_list_widget.list_model)

        get_slide_list_data_action = OnGetSelectedItemsDataAction("get_selected_items", menu_bar,
                                                                  self.slide_list_widget.list_view)
        list_view_menu = ListViewMenu("list_view", menu_bar, self.slide_list_widget)
