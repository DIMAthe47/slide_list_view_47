from PyQt5.QtWidgets import QMainWindow, QActionGroup, QGroupBox, QFormLayout, QHBoxLayout, \
    QLineEdit, QDialogButtonBox, QVBoxLayout, QDialog, QListView
from media_object import media_object_extractors
from media_object_action import OnLoadMediaObjectsAction, OnGetSelectedMediaObjectsDataAction
from media_object_widget import MediaObjectWidget


class MediaObjectMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Media objects')
        self.resize(1500, 600)
        self.media_objects_widget = MediaObjectWidget()
        self.setCentralWidget(self.media_objects_widget)

        menu_bar = self.menuBar()
        load_action_menu = menu_bar.addMenu("load")
        load_action_group = QActionGroup(load_action_menu)
        self.load_actions = {}
        for media_object_extractor_title in media_object_extractors:
            action = OnLoadMediaObjectsAction(load_action_menu, media_object_extractor_title)
            action.setCheckable(True)
            action.set_list_model(self.media_objects_widget.list_model)
            action.set_media_object_extractor(media_object_extractors[media_object_extractor_title])
            load_action_group.addAction(action)
            load_action_menu.addAction(action)
            self.load_actions[media_object_extractor_title] = action

        get_media_objects_data_action = OnGetSelectedMediaObjectsDataAction(menu_bar)
        get_media_objects_data_action.set_list_view(self.media_objects_widget.list_view)
        menu_bar.addAction(get_media_objects_data_action)

        view_actions_menu = menu_bar.addMenu("view_actions")

        media_objects_per_view_action = view_actions_menu.addAction("icon_max_size_or_ratio")
        media_objects_per_view_action.triggered.connect(self.on_media_objects_per_view_action)

        media_objects_per_view_action = view_actions_menu.addAction("change view_mode")
        media_objects_per_view_action.triggered.connect(self.on_change_view_mode)

    def on_change_view_mode(self):
        if self.media_objects_widget.list_view.viewMode() == QListView.IconMode:
            self.media_objects_widget.list_view.setViewMode(QListView.ListMode)
        else:
            self.media_objects_widget.list_view.setViewMode(QListView.IconMode)

    def on_media_objects_per_view_action(self):
        formGroupBox = QGroupBox("icon size or ratio (int or float)")
        horizontal_layout = QHBoxLayout(formGroupBox)
        icon_size_w = QLineEdit(str(self.media_objects_widget.list_view.icon_max_size_or_ratio[0]))
        icon_size_h = QLineEdit(str(self.media_objects_widget.list_view.icon_max_size_or_ratio[1]))
        horizontal_layout.addWidget(icon_size_w)
        horizontal_layout.addWidget(icon_size_h)
        layout = QFormLayout(formGroupBox)
        layout.addRow("icon_size_or_ratio", horizontal_layout)
        formGroupBox.setLayout(layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        dialog = QDialog(self)

        def on_set_icon_size():
            try:
                w = int(icon_size_w.text())
            except:
                w = float(icon_size_w.text())
            try:
                h = int(icon_size_h.text())
            except:
                h = float(icon_size_h.text())
            self.media_objects_widget.list_view.update_icon_max_size_or_ratio((w, h))
            dialog.close()

        buttonBox.accepted.connect(on_set_icon_size)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(formGroupBox)
        mainLayout.addWidget(buttonBox)

        dialog.setLayout(mainLayout)
        dialog.show()
