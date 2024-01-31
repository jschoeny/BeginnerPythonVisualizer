# This Python file uses the following encoding: utf-8
import sys

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QTextBrowser, QSizePolicy

import syntax

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, file_to_visualize, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_to_visualize = file_to_visualize
        self.load_file()
        self.ui.interpretedCode.setColumnWidth(0, 40)
        self.ui.actualCode.setColumnWidth(0, 40)
        self.lineColor = QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Base)
        self.selectedColor = QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Highlight)
        self.selectedColor.setAlpha(75)
        self.set_current_line(0)
    
    def load_file(self):
        with open(self.file_to_visualize) as f:
            for i, line in enumerate(f):
                # Add line as QTreeWidgetItem to interpretedCode and actualCode
                line = line.replace('\t', '  ')
                item = QTreeWidgetItem()
                item.setText(0, str(i + 1))
                item.setTextAlignment(0, Qt.AlignRight)
                item.setFlags(Qt.ItemIsEnabled)
                self.ui.interpretedCode.addTopLevelItem(item)
                self.ui.interpretedCode.setItemWidget(item, 1, self.create_code_browser(line))
                item = item.clone()
                self.ui.actualCode.addTopLevelItem(item)
                self.ui.actualCode.setItemWidget(item, 1, self.create_code_browser(line))

    def create_code_browser(self, line):
        tb = QTextBrowser(self)
        tb.setMarkdown(f"```python\n{line}```")
        tb.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        tb.setFixedHeight(tb.fontMetrics().height() + 10)
        tb.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tb.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tb.setSizeAdjustPolicy(QTextBrowser.AdjustToContents)
        tb.setTextInteractionFlags(Qt.NoTextInteraction)
        tb.setContentsMargins(0, 0, 0, 0)
        tb.setViewportMargins(0, 0, 0, 0)
        tb.setTextColor(QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Text))
        tb.setTextBackgroundColor(QtGui.QColor(0, 0, 0, 0))
        tb.setStyleSheet("border: 0; padding: 0; margin: 0; background-color: transparent;")
        syntax.PythonHighlighter(tb.document(), tb.textColor())
        return tb

    def set_current_line(self, line):
        for i in range(self.ui.interpretedCode.topLevelItemCount()):
            for column in range(2):
                if i == line:
                    self.ui.interpretedCode.topLevelItem(i).setBackground(column, self.selectedColor)
                    self.ui.actualCode.topLevelItem(i).setBackground(column, self.selectedColor)
                else:
                    self.ui.interpretedCode.topLevelItem(i).setBackground(column, self.lineColor)
                    self.ui.actualCode.topLevelItem(i).setBackground(column, self.lineColor)
                

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mainwindow.py <file_to_visualize>")
        sys.exit(1)
    app = QApplication(sys.argv)
    widget = MainWindow(sys.argv[1])
    widget.show()
    sys.exit(app.exec())
