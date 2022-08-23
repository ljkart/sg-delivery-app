import os
import sgtk
from sgtk.platform.qt import QtCore, QtGui


class AssetDataModel(QtCore.QAbstractTableModel):

    def __init__(self, asset_data, parent=None):
        super(AssetDataModel, self).__init__(parent)
        self._asset_data = asset_data
        self._header_data = ["Asset Name", "Type", "Created For", "Published Files"]

    @property
    def asset_data(self):
        return self._asset_data

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            if section < len(self._header_data):
                if len(self._header_data):
                    return self._header_data[section]
                else:
                    return "Not implemented"
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Vertical:
            return section + 1

    def columnCount(self, parent=None):
        return len(self._header_data)

    def rowCount(self, parent=None):
        return len(self._asset_data)

    def flags(self, index):
        if index.column() == 3:
            return QtCore.Qt.ItemIsEditable | super(AssetDataModel, self).flags(index)
        else:
            return super(AssetDataModel, self).flags(index)

    def data(self, index, role):
        if not self._asset_data:
            return super(AssetDataModel, self).data(index, role)
        row = index.row()
        column = index.column()

        if role == QtCore.Qt.DisplayRole:
            if column == 0:
                return self._asset_data[row].code_str
            if column == 1:
                return self._asset_data[row].asset_type_str
            if column == 2:
                return self._asset_data[row].created_for_str
            if column == 3:
                return self._asset_data[row].published_files_data

        return

    def clear_data(self):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount())
        self._asset_data = []
        self.endRemoveRows()
