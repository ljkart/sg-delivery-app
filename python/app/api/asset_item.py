

class AssetItem(object):
    def __init__(self, sg_asset, logger, sg_utils, types_filter):
        self._code = sg_asset['code']
        self._type = sg_asset['sg_asset_type']
        self._sg_utils = sg_utils
        self._created_for = sg_asset["sg_created_for"]
        self._published_files = sg_asset["sg_published_files"]
        self._type_filter = types_filter
        self._logger = logger

    @property
    def code_str(self):
        return self._code

    @property
    def asset_type_str(self):
        return self._type

    @property
    def created_for_str(self):
        return self._created_for['name'] if self._created_for else ""

    @property
    def published_files_str(self):

        return ",".join([pub['name'] for pub in self._published_files] if self._published_files else [])

    @property
    def published_files_data(self):
        data_list = []
        for pub in self._published_files:
            if self.is_valid_pub_file(pub) is None:
                continue
            data_list.append({"name": pub['code'], "type": pub["type"], "id": pub["id"]})
        return data_list

    @published_files_data.setter
    def published_files_data(self, data):
        self._published_files = data

    @property
    def type_filter(self):
        return self._type_filter

    @type_filter.setter
    def type_filter(self, type_filter):
        self._type_filter = type_filter

    def is_valid_pub_file(self, pub_file):
        for each_type in self._type_filter:
            if not each_type["status"]:
                continue
            if each_type["name"] == pub_file["task.Task.step"]["name"]:
                return True

