from PyQt5.QtCore import Qt, QSize, QVariant, QSizeF
from PyQt5.QtWidgets import QMainWindow, QActionGroup, QGroupBox, QFormLayout, QHBoxLayout, \
    QLineEdit, QDialogButtonBox, QVBoxLayout, QDialog, QListView, QAction

from media_objects_47.model.media_object_list_model import imagepath_decoration_func, MediaObjectListModel
from media_objects_47.widgets.on_load_media_objects_action import OnLoadMediaObjectsAction
from media_objects_47.widgets.on_get_selected_media_objects_action import OnGetSelectedMediaObjectsDataAction
from media_objects_47.widgets.media_object_widget import MediaObjectWidget


class MediaObjectMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Media objects')
        self.resize(1500, 600)
        self.media_objects_widget = MediaObjectWidget()
        self.setCentralWidget(self.media_objects_widget)

        menu_bar = self.menuBar()

        load_action_menu = menu_bar.addMenu("load_actions")
        load_action = OnLoadMediaObjectsAction("load", menu_bar)
        load_action.set_list_model(self.media_objects_widget.list_model)
        load_action_menu.addAction(load_action)
        menu_bar.addMenu(load_action_menu)

        get_media_objects_data_action = OnGetSelectedMediaObjectsDataAction(menu_bar)
        get_media_objects_data_action.set_list_view(self.media_objects_widget.list_view)
        menu_bar.addAction(get_media_objects_data_action)

        view_actions_menu = menu_bar.addMenu("view_actions")
        icon_max_size_or_ratio_action = view_actions_menu.addAction("icon_max_size_or_ratio")
        icon_max_size_or_ratio_action.triggered.connect(self.on_icon_max_size_or_ratio_action)

        toggle_decoration_action = view_actions_menu.addAction("toggle decoration")
        toggle_decoration_action.triggered.connect(self.on_toggle_decoration_action)

        change_view_mode_action = view_actions_menu.addAction("change view_mode")
        change_view_mode_action.triggered.connect(self.on_change_view_mode)

    def on_toggle_decoration_action(self):
        list_model = self.media_objects_widget.list_model
        list_model.beginResetModel()
        if self.media_objects_widget.list_model.role_func[Qt.DecorationRole] is None:
            list_model.update_role_func(Qt.DecorationRole, imagepath_decoration_func)
        else:
            list_model.update_role_func(Qt.DecorationRole, None)
        list_model.endResetModel()

    def on_change_view_mode(self):
        if self.media_objects_widget.list_view.viewMode() == QListView.IconMode:
            self.media_objects_widget.list_view.setViewMode(QListView.ListMode)
        else:
            self.media_objects_widget.list_view.setViewMode(QListView.IconMode)

    def on_icon_max_size_or_ratio_action(self):
        formGroupBox = QGroupBox("icon size or ratio (int or float)")
        horizontal_layout = QHBoxLayout(formGroupBox)

        list_model = self.media_objects_widget.list_model
        decoration_size_func = list_model.role_func[MediaObjectListModel.DecorationSizeOrRatioRole]
        if decoration_size_func is not None:
            prev_icon_size = decoration_size_func(False).value()
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
            view = self.media_objects_widget.list_view
            try:
                w = int(icon_size_w.text())
            except:
                w = float(icon_size_w.text())
            try:
                h = int(icon_size_h.text())
            except:
                h = float(icon_size_h.text())

            def decoration_size_func(size_else_ratio=True):
                viewport_size = self.media_objects_widget.list_view.viewport().size()
                if isinstance(w, float):
                    icon_width = viewport_size.width() * w - view.spacing() * 2 - 2
                else:
                    icon_width = w
                if isinstance(h, float):
                    icon_height = viewport_size.height() * h - view.spacing() * 2 - 2
                else:
                    icon_height = h

                if size_else_ratio:
                    icon_size = (icon_width, icon_height)
                else:
                    icon_size = (w, h)

                return QVariant(icon_size)

            list_model = self.media_objects_widget.list_model
            list_model.beginResetModel()
            list_model.update_role_func(MediaObjectListModel.DecorationSizeOrRatioRole, decoration_size_func)
            list_model.endResetModel()
