# This Python file uses the following encoding: utf-8
import sys
import logging
import argparse

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QTextBrowser, QSizePolicy, QFileDialog

import syntax
from steplogger import StepLoggerThread

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    lineUpdated = QtCore.Signal(int, str)
    lineFinished = QtCore.Signal(int)
    stdout = QtCore.Signal(str)
    updateVariable = QtCore.Signal(tuple)
    goToLine = QtCore.Signal(int)

    def __init__(self, file_to_visualize=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.run_icon = QIcon()
        self.continue_icon = QIcon()
        self.stop_icon = QIcon()
        # Check if light or dark mode
        if QApplication.instance().palette().color(QPalette.Window).lightness() < 128:
            self.run_icon.addFile(u":/res/icons/play_dark.png", QSize(), QIcon.Normal, QIcon.Off)
            self.run_icon.addFile(u":/res/icons/play_dark_disabled.png", QSize(), QIcon.Disabled, QIcon.Off)
            self.continue_icon.addFile(u":/res/icons/continue_dark.png", QSize(), QIcon.Normal, QIcon.Off)
            self.continue_icon.addFile(u":/res/icons/continue_dark_disabled.png", QSize(), QIcon.Disabled, QIcon.Off)
            self.stop_icon.addFile(u":/res/icons/stop_dark.png", QSize(), QIcon.Normal, QIcon.Off)
            self.stop_icon.addFile(u":/res/icons/stop_dark_disabled.png", QSize(), QIcon.Disabled, QIcon.Off)
        else:
            self.run_icon.addFile(u":/res/icons/play_light.png", QSize(), QIcon.Normal, QIcon.Off)
            self.run_icon.addFile(u":/res/icons/play_light_disabled.png", QSize(), QIcon.Disabled, QIcon.Off)
            self.continue_icon.addFile(u":/res/icons/continue_light.png", QSize(), QIcon.Normal, QIcon.Off)
            self.continue_icon.addFile(u":/res/icons/continue_light_disabled.png", QSize(), QIcon.Disabled, QIcon.Off)
            self.stop_icon.addFile(u":/res/icons/stop_light.png", QSize(), QIcon.Normal, QIcon.Off)
            self.stop_icon.addFile(u":/res/icons/stop_light_disabled.png", QSize(), QIcon.Disabled, QIcon.Off)
        self.ui.button_start.setIcon(self.run_icon)
        self.ui.button_stop.setIcon(self.stop_icon)

        self.ui.statusbar.showMessage("No file loaded")
        self.ui.button_start.setEnabled(False)
        self.file_to_visualize = file_to_visualize
        self.load_file()
        self.ui.interpretedCode.setColumnWidth(0, 40)
        self.ui.actualCode.setColumnWidth(0, 40)
        self.ui.variables.setColumnWidth(0, 150)
        self.lineColor = QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Base)
        self.selectedColor = QApplication.palette().color(QtGui.QPalette.Active, QtGui.QPalette.Highlight)
        self.selectedColor.setAlpha(75)
        self.set_current_line(-1)
        self.lineUpdated.connect(self.update_line)
        self.goToLine.connect(self.set_current_line)
        self.lineFinished.connect(self.line_finished)
        self.stdout.connect(self.print_to_console)
        self.updateVariable.connect(self.update_variable)
        self.step_logger = StepLoggerThread(self)
        self.step_logger.error.connect(self.print_error)
        self.ui.interpretedCode.verticalScrollBar().valueChanged.connect(
            self.ui.actualCode.verticalScrollBar().setValue)
        self.code_started = False
        self.enable_close_button(True)

    def open_file(self):
        home_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.HomeLocation)
        self.file_to_visualize = QFileDialog.getOpenFileName(self, "Open File", home_dir, "Python Files (*.py)")[0]
        if self.file_to_visualize:
            self.load_file()

    def load_file(self):
        if self.file_to_visualize is None:
            return
        self.ui.interpretedCode.clear()
        self.ui.actualCode.clear()
        try:
            with open(self.file_to_visualize) as f:
                for i, line in enumerate(f):
                    # Add line as QTreeWidgetItem to interpretedCode and actualCode
                    line = line.replace('\t', '  ')
                    item = QTreeWidgetItem()
                    item.setText(0, str(i + 1))
                    item.setTextAlignment(0, Qt.AlignRight)
                    item.setFlags(Qt.ItemIsEnabled)
                    item.setData(1, Qt.UserRole, line)
                    self.ui.interpretedCode.addTopLevelItem(item)
                    self.ui.interpretedCode.setItemWidget(item, 1, self.create_code_browser(line))
                    item = item.clone()
                    self.ui.actualCode.addTopLevelItem(item)
                    self.ui.actualCode.setItemWidget(item, 1, self.create_code_browser(line))
            self.ui.statusbar.showMessage(f"Loaded file: {self.file_to_visualize}")
            self.setWindowFilePath(self.file_to_visualize)
            self.setWindowTitle(f"{self.file_to_visualize.split('/')[-1]} - Beginner Python Visualizer")
            self.ui.button_start.setEnabled(True)
        except FileNotFoundError:
            self.ui.statusbar.showMessage(f"File not found: {self.file_to_visualize}")
            self.setWindowFilePath("")
            self.setWindowTitle("Beginner Python Visualizer")
            self.ui.button_start.setEnabled(False)
            self.ui.interpretedCode.clear()
            self.ui.actualCode.clear()
        except Exception as e:
            self.ui.statusbar.showMessage(f"Error loading file: {self.file_to_visualize}")
            self.setWindowFilePath("")
            self.setWindowTitle("Beginner Python Visualizer")
            self.ui.button_start.setEnabled(False)
            self.ui.interpretedCode.clear()
            self.ui.actualCode.clear()
            print(e)

    def reset_code(self):
        self.ui.interpretedCode.clear()
        for i in range(self.ui.actualCode.topLevelItemCount()):
            item = self.ui.actualCode.topLevelItem(i).clone()
            self.ui.interpretedCode.addTopLevelItem(item)
            line = item.data(1, Qt.UserRole)
            self.ui.interpretedCode.setItemWidget(
                item, 1, self.create_code_browser(line)
            )

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
        # Scroll to the current line
        if line != -1:
            scroll_line = max(0, line - 1)
            if line > self.ui.interpretedCode.topLevelItemCount() / 2:
                scroll_line = min(line + 1, self.ui.interpretedCode.topLevelItemCount() - 1)
            self.ui.interpretedCode.scrollToItem(self.ui.interpretedCode.topLevelItem(scroll_line))
            self.ui.actualCode.scrollToItem(self.ui.actualCode.topLevelItem(scroll_line))

    def update_line(self, line, code):
        if line == -1:
            self.code_finished()
        else:
            (self.ui.interpretedCode.itemWidget(self.ui.interpretedCode.topLevelItem(line), 1)
             .setMarkdown(f"```python\n{code}```"))

    def update_variable(self, variable):
        name, value = variable
        # Check if variable already exists
        for i in range(self.ui.variables.topLevelItemCount()):
            if self.ui.variables.topLevelItem(i).text(0) == name:
                if value is None:
                    self.ui.variables.takeTopLevelItem(i)
                else:
                    self.ui.variables.topLevelItem(i).setText(1, value)
                return

        item = QTreeWidgetItem()
        item.setText(0, name)
        item.setText(1, value)
        self.ui.variables.addTopLevelItem(item)

    def run_button_clicked(self):
        if self.step_logger.isRunning():
            self.step_code()
        else:
            self.start_code()

    def start_code(self):
        self.enable_close_button(False)
        self.ui.button_start.setEnabled(False)
        self.ui.button_start.repaint()
        self.ui.button_load.setEnabled(False)
        self.ui.button_load.repaint()
        self.reset_code()
        self.step_logger.start()

    def step_code(self):
        self.ui.button_start.setEnabled(False)
        self.ui.button_start.repaint()
        self.step_logger.next_step()

    def stop_code(self):
        self.step_logger.stop()
        self.update_line(-1, "")

    def line_finished(self, lineno):
        if not self.code_started:
            self.ui.console.clear()
            self.ui.button_start.setText("Next Step")
            self.ui.button_start.setIcon(self.continue_icon)
            self.ui.button_stop.setEnabled(True)
            self.code_started = True
        self.ui.button_start.setEnabled(True)
        self.set_current_line(lineno)

    def code_finished(self):
        self.ui.statusbar.showMessage("Code finished", 5000)
        self.ui.button_start.setText("Run Code")
        self.ui.button_start.setIcon(self.run_icon)
        self.ui.button_start.setEnabled(True)
        self.ui.button_stop.setEnabled(False)
        self.ui.button_load.setEnabled(True)
        self.enable_close_button(True)
        self.set_current_line(-1)
        self.code_started = False

    def print_error(self, error):
        exctype, value, tb_str = error
        print(f"Error: {exctype}, {value}")
        print(tb_str)
        self.ui.button_start.setText("Run Code")
        self.ui.button_start.setIcon(self.run_icon)
        self.ui.button_start.setEnabled(False)
        self.ui.button_stop.setEnabled(True)

    def print_to_console(self, text):
        if text.strip() != "":
            self.ui.console.append(text)

    def closeEvent(self, event):
        self.ui.centralwidget.setEnabled(False)
        if self.step_logger is not None:
            self.step_logger.stop()
        QMainWindow.closeEvent(self, event)

    def enable_close_button(self, enable):
        if enable:
            self.setWindowFlags(QtCore.Qt.Window |
                                QtCore.Qt.CustomizeWindowHint |
                                QtCore.Qt.WindowMinimizeButtonHint |
                                QtCore.Qt.WindowMaximizeButtonHint |
                                QtCore.Qt.WindowCloseButtonHint)
        else:
            self.setWindowFlags(QtCore.Qt.Window |
                                QtCore.Qt.CustomizeWindowHint |
                                QtCore.Qt.WindowMinimizeButtonHint |
                                QtCore.Qt.WindowMaximizeButtonHint)
        self.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beginner Python Visualizer")
    parser.add_argument('-f', '--file', action='store', help="Loads specified file on startup")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug logging")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)
    if args.file:
        widget = MainWindow(args.file)
    else:
        widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
