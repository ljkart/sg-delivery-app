import sgtk
from sgtk.platform.qt import QtCore, QtGui


class TableSortFilterProxyModel(QtGui.QSortFilterProxyModel):

    def __init__(self, asset_types=None, filter_text=None, logger=None):
        super(TableSortFilterProxyModel, self).__init__()
        self._asset_types = asset_types if asset_types is not None else []
        self._filter_text = filter_text if filter_text is not None else []
        self._logger = logger
        self._pattern = None
        self._filter_column = 0
        self.set_filter("", self._asset_types)

    def filterAcceptsRow(self, row, parent):
        if self._pattern == "" and len(self._asset_types) == 4:
            return True
        model = self.sourceModel()
        asset_name = model.data(model.index(row, 0, parent),
                                QtCore.Qt.DisplayRole)
        asset_type = model.data(model.index(row, 1, parent),
                                QtCore.Qt.DisplayRole)
        if self._pattern in asset_name and asset_type in self._asset_types:
            return True
        else:
            return False

    def set_filter(self, asset_name, asset_types):
        self._pattern = asset_name
        self._asset_types = asset_types
        self.invalidateFilter()
        self.sort(0)
        self.layoutChanged.emit()
