from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QAction, QGroupBox, QHBoxLayout, QLineEdit, QFormLayout, QDialog, QDialogButtonBox, \
    QVBoxLayout, QMenu

from slide_list_view_47.model.role_funcs import decoration_size_func_factory
from slide_list_view_47.model.slide_list_model import SlideListModel
from slide_list_view_47.widgets.slide_list_widget import SlideListWidget


class OnIconMaxSizeOrRatioAction(QAction):
    def __init__(self, title, parent, slide_list_widget):
        super().__init__(title, parent)
        self.window = None
        if isinstance(parent, QMenu):
            self.window = parent.parent()
            parent.addAction(self)
        self.triggered.connect(self.on_icon_max_size_or_ratio_action)
        self.slide_list_widget = slide_list_widget

    def set_data_consumer(self, data_consumer):
        self.data_consumer = data_consumer

    # def set_slide_list_widget(self, slide_list_widget: SlideListWidget):
    #     self.slide_list_widget = slide_list_widget

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

        dialog = QDialog(self.window)
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
