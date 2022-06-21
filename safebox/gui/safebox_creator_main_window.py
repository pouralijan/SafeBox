import sys
from typing import Optional

import PySide6
from PySide6 import QtWidgets
from qt_material import QtStyleTools, list_themes
from safebox.gui.widgets import cycle_generator, CreatorWidget

class MainWindow(QtWidgets.QMainWindow, QtStyleTools):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = ...,
                 flags: PySide6.QtCore.Qt.WindowFlags = ...) -> None:
        super().__init__()
        self.themes = cycle_generator(list_themes())
        self.apply_stylesheet(self, "dark_teal.xml")
        self.setCentralWidget(CreatorWidget(parent=self))
    def change_theme(self):
        self.apply_stylesheet(self, next(self.themes))
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window= MainWindow()
    main_window.show()
    sys.exit(app.exec())