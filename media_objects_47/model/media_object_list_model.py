import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, QSize

from media_objects_47.model.role_funcs import str_display_func, item_func, decoration_size_hint_func


class MediaObjectListModel(QAbstractListModel):
    ItemRole = Qt.UserRole
    DecorationSizeOrRatioRole = Qt.UserRole + 1

    def __init__(self, items=[], display_func=str_display_func, decoration_func=None,
                 edit_func=None, tooltip_func=str_display_func,
                 size_hint_func=None, item_func=item_func, decoration_size_hint_func=decoration_size_hint_func):
        super().__init__()
        self.items = items

        self.role_func = {
            Qt.SizeHintRole: size_hint_func,
            Qt.DisplayRole: display_func,
            Qt.EditRole: edit_func,
            Qt.ToolTipRole: tooltip_func,
            Qt.DecorationRole: decoration_func,
            MediaObjectListModel.ItemRole: item_func,
            MediaObjectListModel.DecorationSizeOrRatioRole: decoration_size_hint_func,
        }

    def update_role_func(self, role, func):
        self.role_func[role] = func

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        item = self.items[index.row()]
        if role in self.role_func:
            custom_handler = self.role_func[role]
            if custom_handler:
                if role == Qt.DecorationRole:
                    icon_size = self.data(index, MediaObjectListModel.DecorationSizeOrRatioRole)
                    decoration = custom_handler(item, QSize(*icon_size.value()))
                    return QVariant(decoration)
                elif role == MediaObjectListModel.DecorationSizeOrRatioRole:
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

    def update_media_objects(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def setData(self, index: QModelIndex, value: typing.Any, role=Qt.DisplayRole) -> bool:
        item = self.items[index.row()]
        if role == Qt.EditRole:
            self.items[index.row()] = value
            self.dataChanged.emit(index, index)
            return True
        return False
