# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dilivery_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..drop_area import DropAreaFrame

import resources_rc
import delivery_resource_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(730, 657)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.large_drop_area = DropAreaFrame(self.page)
        self.large_drop_area.setObjectName(u"large_drop_area")
        self.verticalLayout = QVBoxLayout(self.large_drop_area)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 148, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_5 = QLabel(self.large_drop_area)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 0))
        self.label_5.setMaximumSize(QSize(150, 150))
        self.label_5.setPixmap(QPixmap(u":/tk-multi-delivery/spreadsheet.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.large_drop_area_label = QLabel(self.large_drop_area)
        self.large_drop_area_label.setObjectName(u"large_drop_area_label")
        self.large_drop_area_label.setMaximumSize(QSize(450, 16777215))
        self.large_drop_area_label.setStyleSheet(u"QLabel {\n"
"    font-size: 24px;\n"
"}")
        self.large_drop_area_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.large_drop_area_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 288, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout_2.addWidget(self.large_drop_area, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_3 = QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolButton = QToolButton(self.page_2)
        self.toolButton.setObjectName(u"toolButton")
        icon = QIcon()
        icon.addFile(u":/tk-multi-delivery/gear.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.toolButton)

        self.checkBox = QCheckBox(self.page_2)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_2.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.page_2)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_2.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.page_2)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.horizontalLayout_2.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.page_2)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.horizontalLayout_2.addWidget(self.checkBox_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.tableView = QTableView(self.page_2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_2.addWidget(self.tableView)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_5.setText("")
        self.large_drop_area_label.setText(QCoreApplication.translate("Dialog", u"Drag and drop Asset spreadsheet here", None))
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.checkBox.setText(QCoreApplication.translate("Dialog", u"chr", None))
        self.checkBox_2.setText(QCoreApplication.translate("Dialog", u"prp", None))
        self.checkBox_3.setText(QCoreApplication.translate("Dialog", u"env", None))
        self.checkBox_4.setText(QCoreApplication.translate("Dialog", u"fx", None))
    # retranslateUi

