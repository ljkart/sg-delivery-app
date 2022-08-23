import os
import csv
import io
import sgtk
from tank_vendor.shotgun_api3 import Shotgun


class DeliveryLib(object):
    def __init__(self, logger, status_msg_gui, task_manager):
        self._logger = logger
        self._task_manager = task_manager
        self._status_msg_gui = status_msg_gui
        self._bundle = sgtk.platform.current_bundle()
        self._sg = self._bundle.shotgun

    def validate_spreadsheet(self, spreadsheet):
        if len(spreadsheet) > 1:
            self._logger.warning("More than one CSV selected")
            self._status_msg_gui.setText("More than one CSV selected")
            return
        spreadsheet = spreadsheet[0]
        name, ext = os.path.splitext(spreadsheet)
        if ext != ".csv":
            self._logger.error("{} not a supported spreadsheet , require .csv file".format(spreadsheet))
            self._status_msg_gui.setText("{} not a supported spreadsheet , require .csv file".format(spreadsheet))
            return

        return spreadsheet

    def read_csv(self, spreadsheet):
        data = []
        headers = None
        with io.open(spreadsheet, mode="r", encoding="utf-8-sig") as fh:
            reader = csv.reader(fh)
            for i, row in enumerate(reader):
                # header row
                if i == 0:
                    headers = row
                else:
                    data.append(row)
        return data, headers

    def get_entity_info(self, ids, entity_type, fields, callback=None):
        # create batch filters
        filters = [
            {
                "filter_operator": "any",
                "filters": ids
            }
        ]

        asset_sg_data = self._sg.find(entity_type, filters, fields)

        if callback is not None:
            callback(asset_sg_data)
        else:
            return asset_sg_data




