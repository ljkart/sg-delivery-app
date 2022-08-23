import copy
import os.path
import sys
import sgtk
from sgtk.platform.qt import QtCore, QtGui
from tank_vendor import ruamel_yaml as yaml
from tank_vendor import six
from .ui import delivery_tool_gui
from .ui import filter_options_dialog
from .ui import delivery_ouput_setting_gui
from .progress_status import ProgressStatusLabel
from .api import delivery_lib
from .api import asset_item
from .api import asset_data_model
from .api import pub_file_delegate
from .api import sortfilter_proxy_model

# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)
search_widget = sgtk.platform.import_framework("tk-framework-qtwidgets", "search_widget")
task_manager = sgtk.platform.import_framework("tk-framework-shotgunutils", "task_manager")
# import the shotgun_fields module from the framework
shotgun_fields = sgtk.platform.import_framework("tk-framework-qtwidgets", "shotgun_fields")
shotgun_model = sgtk.platform.import_framework("tk-framework-shotgunutils", "shotgun_model")
config = "{}/config.yaml".format(os.path.abspath(os.path.dirname(__file__)))


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system.

    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Bidaya Delivery Tool", app_instance, AppDialog)


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)

        # now load in the UI that was created in the UI designer
        self.ui = delivery_tool_gui.DeliveryToolGui()
        search_asset_widget = None
        self._delivery_lib = None
        self._spreadsheet = None
        self._table_model = None
        self._proxy_model = None
        self.search_asset_widget = None
        self._filter_settings_btn = None
        self._app_config = None
        self._filter_types = []

        self.ui.setupUi(self)
        self._init_gui()
        self._make_connections()

    def _init_gui(self):
        """
        initialise gui
        """
        self.search_asset_widget = search_widget.SearchWidget(self)
        self.search_asset_widget.setFixedWidth(450)
        self.search_asset_widget.set_placeholder_text("Search Asset")
        self.ui.horizontalLayout_2.addWidget(self.search_asset_widget)
        self.ui.page.setStyleSheet("QWidget#page{border :3px solid #f7e9ff;border-style : dashed}")

        with open(config) as fh:
            self._app_config = yaml.load(fh)
        # set filter types
        self._filter_types = [{"name": opt, "status": self._app_config["filter_types"][opt]} for opt in
                              self._app_config.get("filter_types")]

        # filter settings button
        self.setup_filter_settings_button()

        # hide home button
        self.ui.nav_home_btn.hide()

        # add display features to table view
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.setSortingEnabled(True)

        # status label
        self.status_label = ProgressStatusLabel(self)
        self.status_label.setMinimumWidth(450)
        self.ui.horizontalLayout_3.addWidget(self.status_label)

        # make delivery button
        self.make_delivery_btn = QtGui.QToolButton()
        self.make_delivery_btn.setText("Make Delivery")
        # self.make_delivery_btn.setDisabled(True)
        self.ui.horizontalLayout_3.addWidget(self.make_delivery_btn)

        # task manager
        self._bg_task_manager = task_manager.BackgroundTaskManager(self, True, max_threads=2)
        self._fields_manager = shotgun_fields.ShotgunFieldManager(
            self, bg_task_manager=self._bg_task_manager
        )
        self._fields_manager.initialize()

        # navigation ui
        self._delivery_lib = delivery_lib.DeliveryLib(logger,
                                                      self.status_label,
                                                      self._bg_task_manager)

    def setup_filter_settings_button(self):
        """
        filter button gui setup
        """
        # settings tool
        self._filter_settings_btn = QtGui.QToolButton()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._filter_settings_btn.sizePolicy().hasHeightForWidth())
        self._filter_settings_btn.setSizePolicy(sizePolicy)
        self._filter_settings_btn.setObjectName(u"filter_settings_btn")
        self._filter_settings_btn.setText("step filters")
        self.ui.horizontalLayout_2.addWidget(self._filter_settings_btn)

    def closeEvent(self, event):
        """
        Clean up the object when deleted.
        Args:
            event: qt events

        Returns:
            None
        """


        self._bg_task_manager.shut_down()
        event.accept()

    def _make_connections(self):
        """
        Method to make widget connections
        """
        self.ui.large_drop_area.something_dropped.connect(self._on_drop)
        self.ui.large_drop_area.drag_entered.connect(self._on_drag_enter)
        self.ui.large_drop_area.drag_left.connect(self._on_drag_left)
        self.ui.nav_home_btn.clicked.connect(self._navigate_to_home)
        self.ui.chr_cb.stateChanged.connect(self._on_asset_type_filter_changed)
        self.ui.prp_cb.stateChanged.connect(self._on_asset_type_filter_changed)
        self.ui.env_cb.stateChanged.connect(self._on_asset_type_filter_changed)
        self.ui.fx_cb.stateChanged.connect(self._on_asset_type_filter_changed)
        self._filter_settings_btn.clicked.connect(self._on_filter_button_clicked)
        self.search_asset_widget.search_edited.connect(self._on_search_text_changed)
        self.make_delivery_btn.clicked.connect(self._on_make_delivery_clicked)

    def _navigate_to_home(self):
        """
        Navigate to Home screen
        """
        self.ui.page.setStyleSheet("QWidget#page{border :3px solid #f7e9ff;border-style : dashed}")
        self.ui.progressbar.setValue(0)
        # self._bg_task_manager.stop_all_tasks()
        # if self._table_model is not None:
        #     self._table_model.clear_data()
        self.status_label.setText("")
        self.ui.stackedWidget.setCurrentIndex(0)

    def _on_drop(self, files):
        """
        Called when something dropped here
        Args:
            files: list of files dropped

        Returns: None
        """
        str_files = [six.ensure_str(f) for f in files]
        logger.info("Dropped items --- {}".format(str_files))
        self._prepare_asset_list_page(str_files)

    def _prepare_asset_list_page(self, spreadsheet):
        """

        Args:
            spreadsheet:

        Returns:

        """

        self._set_page(1)
        self.ui.progressbar.setValue(0)
        self.ui.chr_cb.setChecked(True)
        self.ui.prp_cb.setChecked(True)
        self.ui.env_cb.setChecked(True)
        self.ui.fx_cb.setChecked(True)
        self.status_label.setText("Dropped Spreadsheet {} ".format(spreadsheet))
        stat = self._delivery_lib.validate_spreadsheet(spreadsheet)
        if spreadsheet is not None:
            self._spreadsheet = stat
            self._populate_table()

    def _set_page(self, index):
        """
        set stacked page
        Args:
            index: qt page index

        Returns:None

        """
        self.ui.stackedWidget.setCurrentIndex(index)

    def _on_drag_enter(self, e):
        """
        on entering drag area
        Args:
            e: event

        Returns: None
        """

        logger.info("enter {} ".format(e))
        self.ui.page.setStyleSheet("QWidget#page{border :3px solid #ffd3f8;border-style : solid; border-radius: 5px}")

    def _on_drag_left(self, e):
        """
        on leafing drag area
        Args:
            e: qt event

        Returns: None

        """
        logger.info("left {} ".format(e))
        self.ui.page.setStyleSheet("QWidget#page{border :3px solid #f7e9ff;border-style : dashed}")

    def _populate_table(self):
        """
        Method to populate table
        Returns:None

        """
        asset_data, asset_data_headers = self._delivery_lib.read_csv(self._spreadsheet)
        self.progressbar_advance()
        self.status_label.setText("Reading CSV Done..")
        try:
            asset_name_index = asset_data_headers.index('Asset Name')
            asset_id_index = asset_data_headers.index('Id')
            asset_project_index = asset_data_headers.index('Project')

        except ValueError as e:
            msg = "No Asset Name or Id found in the asset spreadsheet. Asset Name, Id, Project required"
            self.status_label.setText(msg)
            raise Exception(msg)

        asset_ids = [['id', 'is', int(asset[asset_id_index])] for asset in asset_data]
        fields = ["code", "sg_created_for", "sg_asset_type", "sg_published_files"]
        self._bg_task_manager.add_task(
            self._delivery_lib.get_entity_info,
            task_args=[asset_ids, "Asset",  fields, self._prepare_table_data]
        )

    def progressbar_advance(self):
        """
        advance progress bar by 10
        Returns:None

        """
        self.ui.progressbar.setValue(self.ui.progressbar.value() + 10)

    def progressbar_set_completed(self):
        """
        Set progress bar completed
        Returns: None

        """
        self.ui.progressbar.setValue(100)

    def _prepare_table_data(self, sg_data=None):
        """
        Prepare table data with sg informations
        Args:
            sg_data: sg info about dropped asset list

        Returns: None

        """
        self.status_label.setText("Fetched SG Asset Data..")
        self.progressbar_advance()
        self._formulate_published_files_data(sg_data)

    def _show_table_data(self, sg_asset_data):
        """
        Show table from the dropped CSV
        Args:
            sg_asset_data: populated sg asset entity info

        Returns: NOne

        """
        sg_asset_data = sorted(sg_asset_data, key=lambda x: x['code'])
        self._table_model = asset_data_model.AssetDataModel([asset_item.AssetItem(asset,
                                                                                  logger,
                                                                                  self._delivery_lib,
                                                                                  self._filter_types)
                                                             for asset in sg_asset_data],
                                                            self)
        self.status_label.setText("Prepared Table Model..")
        self.progressbar_advance()
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.verticalHeader().setVisible(True)

        # # set model for the table with asset items
        asset_pub_class_widget_display = self._fields_manager.get_class("Asset",
                                                                        "sg_published_files",
                                                                        self._fields_manager.DISPLAY)
        asset_pub_class_widget_editor = self._fields_manager.get_class("Asset",
                                                                       "sg_published_files",
                                                                       self._fields_manager.EDITOR)
        pub_delegate = pub_file_delegate.PubFileDelegate(parent=self.ui.tableView,
                                                         logger=logger,
                                                         display_class=asset_pub_class_widget_display,
                                                         editor_class=asset_pub_class_widget_editor)
        self.ui.tableView.setItemDelegateForColumn(3, pub_delegate)
        self.status_label.setText("Setting Proxy Model..")
        checked_asset_types = self._get_checked_asset_types()
        self._proxy_model = sortfilter_proxy_model.TableSortFilterProxyModel(checked_asset_types,
                                                                             self.search_asset_widget.search_text,
                                                                             logger)
        self._proxy_model.setSourceModel(self._table_model)
        self.ui.tableView.setModel(self._proxy_model)
        self.status_label.setText("Prepared Asset Table Successfully..")
        self.progressbar_set_completed()

    def _get_checked_asset_types(self):
        """
        get filter types of assets tasks
        Returns: list

        """
        asset_types = []

        if self.ui.chr_cb.isChecked():
            asset_types.append("Character")
        if self.ui.prp_cb.isChecked():
            asset_types.append("Prop")
        if self.ui.env_cb.isChecked():
            asset_types.append("Environment")
        if self.ui.fx_cb.isChecked():
            asset_types.append("FX")

        return asset_types

    def _on_search_text_changed(self, pattern):
        """
        call when search pattern changed
        Args:
            pattern: search input

        Returns: None

        """
        if self._proxy_model is not None:
            self._proxy_model.set_filter(pattern, self._get_checked_asset_types())

    def _on_asset_type_filter_changed(self):
        """
        calls when asset type filter changed
        Returns: None

        """
        if self._proxy_model is not None:
            self._proxy_model.set_filter(self.search_asset_widget.search_text, self._get_checked_asset_types())

    def _on_filter_button_clicked(self):
        """
        open asset task filter menu
        Returns: NOne

        """
        f_dialog = filter_options_dialog.FilterOptions(self, self._filter_types)
        f_dialog.show()

    def on_filter_types_changed(self, filter_type, status):
        """
        calls when any filter types status changed
        Args:
            filter_type: asset filter type
            status: asset filter type status

        Returns: None

        """
        if self._filter_types is not None:
            for each in self._filter_types:
                if each["name"] == filter_type:
                    each["status"] = 1 if status == 2 else 0
                    logger.info("status_updated {} ".format(self._filter_types))

    def on_filter_types_updated(self):
        """
        calls when filter type applied
        Returns: None

        """
        for asset_item in self._table_model.asset_data:
            asset_item.type_filter = self._filter_types
        self._table_model.layoutChanged.emit()
        self.status_label.setText("Filter Applied")

    def _formulate_published_files_data(self, sg_data):
        """
        Method used to formulate all list of published files from the list assets with filter types applied.
        This is helpful to make one query to get all list of published files and can use later to filter them
        Args:
            sg_data: SG published files data

        Returns: None

        """
        pub_files_ids = []
        new_sg_data = copy.copy(sg_data)
        fields = ["code", "task", "task.Task.step", "entity"]
        self.progressbar_advance()
        for each_asset in sg_data:
            pub_ids = [['id', 'is', int(pub["id"])] for pub in each_asset['sg_published_files']]
            pub_files_ids.extend(pub_ids)
        self.status_label.setText("Fetching published files data..")
        sg_pub_files_data = self._delivery_lib.get_entity_info(pub_files_ids, "PublishedFile", fields)
        for each_asset in new_sg_data:
            entity_id = each_asset["id"]
            each_asset['sg_published_files'] = []
            for each_pub in sg_pub_files_data:
                if entity_id == each_pub['entity']['id']:
                    each_asset["sg_published_files"].append(each_pub)

        self.progressbar_advance()
        self._show_table_data(new_sg_data)

    def _on_make_delivery_clicked(self):
        """
        Execute actual asset delivery
        Returns: None

        """
        logger.info("Making Delivery")
        self.status_label.setText("Preparing Delivery")
        del_output_gui = delivery_ouput_setting_gui.DeliveryOutputSettingsGui(self, self._app_config, logger)
        del_output_gui.show()









