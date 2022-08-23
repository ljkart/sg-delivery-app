
from sgtk.platform.qt import QtCore, QtGui


class FilterOptions(QtGui.QDialog):
    def __init__(self, parent, option_list):
        super(FilterOptions, self).__init__(parent)
        self.resize(100, 400)
        self._parent_gui = parent
        self._central_layout = QtGui.QVBoxLayout()
        self.setLayout(self._central_layout)
        self._options = option_list
        self._set_options()
        self._apply_btn = QtGui.QPushButton()
        self._apply_btn.setText("Apply")
        self._apply_btn.clicked.connect(self._on_apply_btn_clicked)
        self._central_layout.addWidget(self._apply_btn)

    def _set_options(self):
        for each_item in self._options:
            item = QtGui.QCheckBox()
            item.setText(each_item["name"])
            item.setChecked(each_item["status"])
            item.stateChanged.connect(self._on_filter_type_changed)
            self._central_layout.addWidget(item)

    def _on_filter_type_changed(self, state):
        self._parent_gui.on_filter_types_changed(self.sender().text(), state)

    def _on_apply_btn_clicked(self):
        self._parent_gui.on_filter_types_updated()
        self.close()


