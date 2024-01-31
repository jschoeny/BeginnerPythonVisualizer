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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGroupBox, QHBoxLayout,
    QHeaderView, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTextBrowser,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

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

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer_5 = QSpacerItem(80, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.console = QTextBrowser(self.groupBox_3)
        self.console.setObjectName(u"console")

        self.verticalLayout_3.addWidget(self.console)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Interpreted Code", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Original Code", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Next Line", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Output", None))
    # retranslateUi

