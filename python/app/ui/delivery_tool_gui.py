from sgtk.platform.qt import QtCore, QtGui
from ..drop_area import DropAreaFrame
import delivery_resource


class DeliveryToolGui(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"DeliveryToolGui")
        Dialog.resize(1503, 900)

        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QtGui.QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QtGui.QWidget()

        self.page.setObjectName(u"page")
        self.page.setStyleSheet("QWidget#page{border :3px solid #f7e9ff;border-style : dashed}")
        self.gridLayout_2 = QtGui.QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.large_drop_area = DropAreaFrame(self.page)
        # self.large_drop_area.setFrameShape(QtGui.QFrame.StyledPanel)
        # self.large_drop_area.setFrameShadow(QtGui.QFrame.Raised)
        self.large_drop_area.setFocusPolicy(QtCore.Qt.NoFocus)


        self.verticalLayout = QtGui.QVBoxLayout(self.large_drop_area)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QtGui.QSpacerItem(20, 148, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.label_5 = QtGui.QLabel(self.large_drop_area)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QtCore.QSize(150, 150))
        self.label_5.setMaximumSize(QtCore.QSize(150, 150))
        self.label_5.setPixmap(QtGui.QPixmap(u":/tk-multi-delivery/spreadsheet.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_5)
        self.large_drop_area_label = QtGui.QLabel(self.large_drop_area)
        self.large_drop_area_label.setText("Drop Asset Spreadsheet Here")
        self.large_drop_area_label.setObjectName(u"large_drop_area_label")
        self.large_drop_area_label.setStyleSheet(u"QLabel {\n"
                                                 "    font-size: 24px;\n"
                                                 "}")
        self.large_drop_area_label.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.large_drop_area_label)

        self.horizontalSpacer_2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QtGui.QSpacerItem(20, 288, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.gridLayout_2.addWidget(self.large_drop_area, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.nav_home_btn = QtGui.QToolButton()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_home_btn.sizePolicy().hasHeightForWidth())
        self.nav_home_btn.setSizePolicy(sizePolicy)
        self.nav_home_btn.setObjectName(u"nav_home_btn")
        self.nav_home_btn.setMinimumSize(QtCore.QSize(39, 36))
        self.nav_home_btn.setMaximumSize(QtCore.QSize(39, 36))
        self.nav_home_btn.setBaseSize(QtCore.QSize(0, 0))
        self.nav_home_btn.setStyleSheet("#nav_home_btn{\n"
                                        "   border: none;\n"
                                        "   background-color: none;\n"
                                        "   background-repeat: no-repeat;\n"
                                        "   background-position: center center;\n"
                                        "   background-image: url(:/tk-multi-delivery/home.png);\n"
                                        "}\n"
                                        "\n"
                                        "#nav_home_btn:disabled{\n"
                                        "   background-image: url(:/tk-multi-delivery/home_disabled.png);\n"
                                        "}\n"
                                        "\n"
                                        "#nav_home_btn:hover{\n"
                                        "background-image: url(:/tk-multi-delivery/home_hover.png);\n"
                                        "}\n"
                                        "\n"
                                        "#nav_home_btn:Pressed {\n"
                                        "background-image: url(:/tk-multi-delivery/home_pressed.png);\n"
                                        "}\n"
                                        "")
        self.nav_home_btn.setText("")
        self.horizontalLayout_2.addWidget(self.nav_home_btn)



        self.chr_cb = QtGui.QCheckBox(self.page_2)
        self.chr_cb.setText("chr")
        self.horizontalLayout_2.addWidget(self.chr_cb)


        self.prp_cb = QtGui.QCheckBox(self.page_2)
        self.prp_cb.setText("prp")
        self.horizontalLayout_2.addWidget(self.prp_cb)

        self.env_cb = QtGui.QCheckBox(self.page_2)
        self.env_cb.setText("env")
        self.horizontalLayout_2.addWidget(self.env_cb)

        self.fx_cb = QtGui.QCheckBox(self.page_2)
        self.fx_cb.setText("fx")
        self.horizontalLayout_2.addWidget(self.fx_cb)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.tableView = QtGui.QTableView(self.page_2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_2.addWidget(self.tableView)

        # progress bar
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.progressbar = QtGui.QProgressBar()
        self.progressbar.setMaximumHeight(30)
        self.progressbar.setMaximumWidth(250)
        self.horizontalLayout_3.addWidget(self.progressbar)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        self.stackedWidget.setCurrentIndex(0)



