import os

from sgtk.platform.qt import QtCore, QtGui


class DeliveryOutputSettingsGui(QtGui.QDialog):
    def __init__(self, parent, config, logger):
        super(DeliveryOutputSettingsGui, self).__init__(parent)
        self.resize(750, 200)
        self._app_config = config
        self._parent_gui = parent
        self._logger = logger
        self._central_layout = QtGui.QVBoxLayout()
        self.setLayout(self._central_layout)

        # asset folder name folder
        asset_folder_name_layout = QtGui.QHBoxLayout()
        self._central_layout.addLayout(asset_folder_name_layout)
        asset_folder_label = QtGui.QLabel()
        asset_folder_label.setMinimumWidth(150)
        asset_folder_label.setText("Asset Folder Name")
        self._asset_folder_field = QtGui.QLineEdit()
        self._asset_folder_field.setText(self._app_config["output_folders"]["asset"])
        asset_folder_name_layout.addWidget(asset_folder_label)
        asset_folder_name_layout.addWidget(self._asset_folder_field)

        # output path
        output_path_layout = QtGui.QHBoxLayout()
        self._central_layout.addLayout(output_path_layout)
        output_path_label = QtGui.QLabel()
        output_path_label.setMinimumWidth(150)
        output_path_label.setText("Delivery Root Folder")
        self._output_path_field = QtGui.QLineEdit()
        output_path_layout.addWidget(output_path_label)
        output_path_layout.addWidget(self._output_path_field)

        #delivery button
        self._make_delivery_btn = QtGui.QPushButton()
        self._make_delivery_btn.setText("Execute")
        self._make_delivery_btn.clicked.connect(self._on_execute_clicked_clicked)
        self._central_layout.addWidget(self._make_delivery_btn)

    def _on_execute_clicked_clicked(self):
        if not self._is_valid_delivery():
            return
        self._logger.info("Making Delivery")

    def _is_valid_delivery(self):
        # check output path exists
        if not os.path.exists(self._output_path_field.text()):
            self._parent_gui.status_label.setText("Output Root Folder :  {} doesn't "
                                                  "exists".format(self._output_path_field.text()))
            self._logger.error("Output Root Folder :  {} doesn't "
                               "exists".format(self._output_path_field.text())
                               )
            return

        return True



