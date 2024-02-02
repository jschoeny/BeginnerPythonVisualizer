# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(350, 300))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.interpretedCode = QTreeWidget(self.groupBox)
        self.interpretedCode.headerItem().setText(0, "")
        self.interpretedCode.headerItem().setText(1, "")
        self.interpretedCode.setObjectName(u"interpretedCode")
        self.interpretedCode.setEnabled(True)
        font = QFont()
        font.setFamilies([u"Courier New"])
        self.interpretedCode.setFont(font)
        self.interpretedCode.setFocusPolicy(Qt.WheelFocus)
        self.interpretedCode.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.interpretedCode.setDragEnabled(False)
        self.interpretedCode.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.interpretedCode.setIndentation(0)
        self.interpretedCode.setRootIsDecorated(False)
        self.interpretedCode.setItemsExpandable(True)
        self.interpretedCode.setHeaderHidden(True)
        self.interpretedCode.setExpandsOnDoubleClick(False)
        self.interpretedCode.header().setVisible(False)

        self.verticalLayout.addWidget(self.interpretedCode)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(350, 300))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.actualCode = QTreeWidget(self.groupBox_2)
        self.actualCode.headerItem().setText(0, "")
        self.actualCode.headerItem().setText(1, "")
        self.actualCode.setObjectName(u"actualCode")
        self.actualCode.setEnabled(True)
        self.actualCode.setFont(font)
        self.actualCode.setMouseTracking(False)
        self.actualCode.setFocusPolicy(Qt.WheelFocus)
        self.actualCode.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.actualCode.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.actualCode.setIndentation(0)
        self.actualCode.setRootIsDecorated(False)
        self.actualCode.setItemsExpandable(True)
        self.actualCode.setHeaderHidden(True)
        self.actualCode.setExpandsOnDoubleClick(False)
        self.actualCode.header().setVisible(False)

        self.verticalLayout_2.addWidget(self.actualCode)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.button_start = QPushButton(self.centralwidget)
        self.button_start.setObjectName(u"button_start")
        self.button_start.setEnabled(True)
        self.button_start.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.button_start)

        self.horizontalSpacer_5 = QSpacerItem(80, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.button_stop = QPushButton(self.centralwidget)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setEnabled(False)
        self.button_stop.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.button_stop)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.groupBox_3.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.console = QTextBrowser(self.groupBox_3)
        self.console.setObjectName(u"console")
        self.console.setFont(font)

        self.verticalLayout_3.addWidget(self.console)


        self.horizontalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(300, 200))
        self.gridLayout = QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.variables = QTreeWidget(self.groupBox_4)
        self.variables.setObjectName(u"variables")
        self.variables.setAnimated(True)

        self.gridLayout.addWidget(self.variables, 0, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.groupBox_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.button_start.clicked.connect(MainWindow.run_button_clicked)
        self.button_stop.clicked.connect(MainWindow.stop_code)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Interpreted Code", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Original Code", None))
        self.button_start.setText(QCoreApplication.translate("MainWindow", u"Run Code", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Output", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Variables in Scope", None))
        ___qtreewidgetitem = self.variables.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Value", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Variable", None));
    # retranslateUi

