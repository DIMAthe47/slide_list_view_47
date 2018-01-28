from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QActionGroup, QGroupBox, QFormLayout, QHBoxLayout, \
    QLineEdit, QDialogButtonBox, QVBoxLayout, QDialog, QListView, QAction, QStyledItemDelegate

from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.model.role_funcs import item_func, slideviewparams_decoration_func, \
    decoration_size_func_factory
from slide_list_view_47.widgets.actions.on_load_items_action import OnLoadItemsAction
from slide_list_view_47.widgets.actions.on_get_selected_items_action import OnGetSelectedItemsDataAction
from slide_list_view_47.widgets.slide_list_widget import SlideListWidget
from slide_list_view_47.widgets.slide_viewer_delegate import SlideViewerDelegate


class SlideListMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Slide list')
        self.resize(1500, 600)
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
        icon_max_size_or_ratio_action = view_actions_menu.addAction("icon_max_size_or_ratio")
        icon_max_size_or_ratio_action.triggered.connect(self.on_icon_max_size_or_ratio_action)

        change_view_mode_action = view_actions_menu.addAction("change view_mode")
        change_view_mode_action.triggered.connect(self.on_change_view_mode)

        action_group = QActionGroup(self)
        self.text_mode_action = QAction("text", action_group)
        self.text_mode_action.setCheckable(True)
        self.text_mode_action.triggered.connect(self.on_text_mode_action)

        self.decoration_mode_action = QAction("text+decoration", action_group)
        self.decoration_mode_action.setCheckable(True)
        self.decoration_mode_action.triggered.connect(self.on_decoration_mode_action)
        self.delegate_mode_action = QAction("slide_viewer_delegate", action_group)
        self.delegate_mode_action.setCheckable(True)
        self.delegate_mode_action.triggered.connect(self.on_delegate_mode_action)

        view_actions_menu.addAction(self.text_mode_action)
        view_actions_menu.addAction(self.decoration_mode_action)
        view_actions_menu.addAction(self.delegate_mode_action)

    def on_text_mode_action(self):
        self.change_mode(QStyledItemDelegate(self), None, None)

    def on_decoration_mode_action(self):
        self.change_mode(QStyledItemDelegate(self), None, slideviewparams_decoration_func)

    def on_delegate_mode_action(self):
        self.change_mode(SlideViewerDelegate(self), item_func, None)

    def change_mode(self, item_delegate, edit_role_func, decoration_role_func):
        list_model = self.slide_list_widget.list_model
        list_model.beginResetModel()
        self.slide_list_widget.list_model.update_role_func(Qt.EditRole, edit_role_func)
        list_model.update_role_func(Qt.DecorationRole, decoration_role_func)
        self.slide_list_widget.list_view.setItemDelegate(item_delegate)
        list_model.endResetModel()

    def on_change_view_mode(self):
        if self.slide_list_widget.list_view.viewMode() == QListView.IconMode:
            self.slide_list_widget.list_view.setViewMode(QListView.ListMode)
        else:
            self.slide_list_widget.list_view.setViewMode(QListView.IconMode)

    def on_icon_max_size_or_ratio_action(self):
        formGroupBox = QGroupBox("icon size or ratio (int or float)")
        horizontal_layout = QHBoxLayout(formGroupBox)

        list_model = self.slide_list_widget.list_model
        decoration_size_func = list_model.role_func[SlideListModel.DecorationSizeOrRatioRole]
        if decoration_size_func is not None:
            prev_icon_size = decoration_size_func(False)
        else:
            prev_icon_size = QSize(200, 200)
        icon_size_w = QLineEdit(str(prev_icon_size[0]))
        icon_size_h = QLineEdit(str(prev_icon_size[1]))
        horizontal_layout.addWidget(icon_size_w)
        horizontal_layout.addWidget(icon_size_h)
        layout = QFormLayout(formGroupBox)
        layout.addRow("icon_size_or_ratio", horizontal_layout)
        formGroupBox.setLayout(layout)

        dialog = QDialog(self)
        dialog.setWindowTitle("Icon size or proportion of viewport size")
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(formGroupBox)
        mainLayout.addWidget(button_box)
        dialog.setLayout(mainLayout)

        res = dialog.exec()
        if res == QDialog.Accepted:
            view = self.slide_list_widget.list_view
            try:
                w = int(icon_size_w.text())
            except:
                w = float(icon_size_w.text())
            try:
                h = int(icon_size_h.text())
            except:
                h = float(icon_size_h.text())

            decoration_size_func = decoration_size_func_factory(view, w, h)

            list_model = self.slide_list_widget.list_model
            list_model.beginResetModel()
            list_model.update_role_func(SlideListModel.DecorationSizeOrRatioRole, decoration_size_func)
            list_model.endResetModel()
