# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem

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
    
    def load_file(self):
        with open(self.file_to_visualize) as f:
            for i, line in enumerate(f):
                # Add line as QTreeWidgetItem to interpretedCode and actualCode
                item = QTreeWidgetItem([i + 1, line])
                self.ui.interpretedCode.addTopLevelItem(item)
                item = QTreeWidgetItem([i + 1, line])
                self.ui.actualCode.addTopLevelItem(item)
                

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mainwindow.py <file_to_visualize>")
        sys.exit(1)
    app = QApplication(sys.argv)
    widget = MainWindow(sys.argv[1])
    widget.show()
    sys.exit(app.exec())
