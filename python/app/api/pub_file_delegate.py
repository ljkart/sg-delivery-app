import sgtk
from sgtk.platform.qt import QtCore, QtGui
shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_model"
)


class PubFileDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent=None, logger=None, display_class=None, editor_class=None, task_manager=None):
        super(PubFileDelegate, self).__init__(parent)
        self._parent = parent
        self._logger = logger
        self._bg_task_manager = task_manager
        self._editor_class = editor_class
        self._display_class = display_class
        self._editor_widget_inst = None
        self._display_widget_inst = None
        self._entity_type = "Asset"
        self._field_name = "sg_published_files"
        self._logger.info("Delegate initiated")

    def createEditor(self, parent, option, index):
        if not index.isValid():
            return
        self._editor_widget_inst = self._create_editor_widget(index, parent)
        data = index.data(QtCore.Qt.DisplayRole)
        self._editor_widget_inst.blockSignals(True)
        self._editor_widget_inst.set_value(data)
        self._editor_widget_inst.blockSignals(False)
        return self._editor_widget_inst

    def setEditorData(self, editor, index):
        self._set_widget_value(editor, index)

    #
    def setModelData(self, editor, model, index):
        src_index = self._map_to_source(index)
        if not src_index or not src_index.isValid():
            # invalid index, do nothing
            return
        model = src_index.model()
        row = src_index.row()
        asset_item = model.asset_data[row]
        # compare the new/old values to see if there is a change
        new_value = editor.get_value()
        cur_value = src_index.data(QtCore.Qt.DisplayRole)
        if cur_value == new_value:
            # value didn't change. nothing to do here.
            return

        asset_item.published_files_data = new_value

    def updateEditorGeometry(self, editor, option, index):
        self._editor_widget_inst.setGeometry(option.rect)

    def paint(self, painter, option, index):
        data = index.data(QtCore.Qt.DisplayRole)
        self._display_widget_inst = self._display_class(self._parent)
        self._display_widget_inst.blockSignals(True)
        self._display_widget_inst.set_value(data)
        self._display_widget_inst.blockSignals(False)

        self._display_widget_inst.setGeometry(option.rect)
        painter.save()
        self._display_widget_inst.resize(option.rect.size())
        painter.translate(option.rect.topLeft())
        self._display_widget_inst.render(painter, QtCore.QPoint(0, 0), renderFlags=QtGui.QWidget.DrawChildren)
        painter.restore()

    def _create_editor_widget(self, model_index, parent):
        if not model_index.isValid():
            return None
        widget = self._editor_class(
            parent=parent,
            entity_type=self._entity_type,
            field_name=self._field_name,
            bg_task_manager=self._bg_task_manager,
            delegate=True,
        )
        widget.setAutoFillBackground(True)
        return widget

    def _set_widget_value(self, widget, model_index):
        src_index = self._map_to_source(model_index)
        if not src_index or not src_index.isValid():
            # invalid index, do nothing
            return

        value = src_index.data(QtCore.Qt.DisplayRole)

        widget.set_value(shotgun_model.sanitize_qt(value))

    @staticmethod
    def _map_to_source(idx, recursive=True):
        src_idx = idx
        while src_idx.isValid() and isinstance(src_idx.model(), QtGui.QAbstractProxyModel):
            src_idx = src_idx.model().mapToSource(src_idx)
            if not recursive:
                break
        return src_idx

