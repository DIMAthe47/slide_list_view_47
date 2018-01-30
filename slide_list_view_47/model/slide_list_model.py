from numbers import Number
from typing import Callable, Any, Tuple

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QSize
from PyQt5.QtGui import QPixmap

from slide_list_view_47.model.role_funcs import item_func, decoration_size_hint_func, \
    slideviewparams_to_str, item_setter
from slide_viewer_47.common.slide_view_params import SlideViewParams


class SlideListModel(QAbstractListModel):
    ItemRole = Qt.UserRole
    DecorationSizeOrRatioRole = Qt.UserRole + 1
    SlideViewParamsRole = Qt.UserRole + 2

    def __init__(self, items=[],
                 display_func: Callable[[Any], str] = slideviewparams_to_str,
                 decoration_func: Callable[[Any, QSize], QPixmap] = None,
                 tooltip_func: Callable[[Any], str] = None,
                 size_hint_func: Callable[[Any], QSize] = None,
                 slide_view_params_func: Callable[[Any], SlideViewParams] = item_func,
                 # slide_view_params_getter: Callable[[Any], SlideViewParams] = item_func,
                 slide_view_params_setter: Callable[[SlideViewParams], None] = item_setter,
                 decoration_size_hint_func: Callable[[Any, ], Tuple[Number, Number]] = decoration_size_hint_func):
        # assuming by default item is of type SlideViewParams
        super().__init__()
        self.items = items
        # self.slide_view_params_setter = slide_view_params_setter
        # self.slide_view_params_getter = slide_view_params_setter

        self.role_func = {
            Qt.SizeHintRole: size_hint_func,
            Qt.DisplayRole: display_func,
            Qt.EditRole: None,
            Qt.ToolTipRole: tooltip_func,
            Qt.DecorationRole: decoration_func,
            SlideListModel.ItemRole: item_func,
            SlideListModel.DecorationSizeOrRatioRole: decoration_size_hint_func,
            SlideListModel.SlideViewParamsRole: slide_view_params_func
        }

    def text_mode(self, item_to_str: Callable[[Any], str]):
        self.update_role_func(Qt.DisplayRole, item_to_str)
        self.update_role_func(Qt.DecorationRole, None)
        self.update_role_func(SlideListModel.SlideViewParamsRole, None)
        self.update_role_func(Qt.EditRole, None)


    def decoration_mode(self, item_to_str: Callable[[Any], str], item_to_pixmap: Callable[[Any], QPixmap]):
        self.update_role_func(Qt.DisplayRole, item_to_str)
        self.update_role_func(Qt.DecorationRole, item_to_pixmap)
        self.update_role_func(SlideListModel.SlideViewParamsRole, None)
        self.update_role_func(Qt.EditRole, None)

    # def slideviewparams_mode(self, item_to_str: Callable[[Any], str],
    #                          slideviewparams_getter: Callable[[Any], SlideViewParams],
    #                          slideviewparams_setter: Callable[[QModelIndex, ],]):
    #     pass

    def slideviewparams_mode(self, item_to_str: Callable[[Any], str],
                             item_to_slideviewparams: Callable[[Any], SlideViewParams]):
        self.update_role_func(Qt.DisplayRole, item_to_str)
        self.update_role_func(Qt.DecorationRole, None)
        self.update_role_func(SlideListModel.SlideViewParamsRole, item_to_slideviewparams)
        self.update_role_func(Qt.EditRole, item_to_slideviewparams)

    def update_role_func(self, role, func):
        # if role == SlideListModel.SlideViewParamsRole:
        #     self.role_func[Qt.EditRole] = func
        self.role_func[role] = func

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        item = self.items[index.row()]
        if role in self.role_func:
            custom_handler = self.role_func[role]
            if custom_handler:
                if role == Qt.DecorationRole:
                    icon_size = self.data(index, SlideListModel.DecorationSizeOrRatioRole)
                    decoration = custom_handler(item, QSize(*icon_size.value()))
                    return QVariant(decoration)
                elif role == SlideListModel.DecorationSizeOrRatioRole:
                    icon_size = custom_handler()
                    return QVariant(icon_size)
                else:
                    role_value = custom_handler(item)
                    return QVariant(role_value)
        return QVariant()

    def flags(self, index):
        if self.role_func[Qt.EditRole] is not None:
            return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def update_items(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def setData(self, index: QModelIndex, value: Any, role=Qt.DisplayRole) -> bool:
        item = self.items[index.row()]
        if role == Qt.EditRole:
            slide_view_params = self.data(index, SlideListModel.SlideViewParamsRole).value()
            slide_view_params.__dict__.update(value.__dict__)
            # self.slide_view_params_setter(self.items, index, value)
            # self.setData(index,value, SlideListModel.SlideViewParamsRole)
            # self.items[index.row()] = value
            self.dataChanged.emit(index, index)
            return True
        return False
