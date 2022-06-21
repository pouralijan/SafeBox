from os import device_encoding
from tabnanny import check
import PySide6
from PySide6 import QtCore, QtWidgets
from typing import Optional

from qt_material import QtStyleTools, list_themes

from safebox.core.utils import get_dev_name
from safebox.core.safebox import SafeBox

class Dialog(QtWidgets.QDialog):
    def __init__(self, title, device, parent: Optional[PySide6.QtWidgets.QWidget] = ..., f: PySide6.QtCore.Qt.WindowFlags = ...) -> None:
        super().__init__(parent)
        
        self.setWindowTitle("GetPassword")

        buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        buttons_box = QtWidgets.QDialogButtonBox(buttons)
        buttons_box.accepted.connect(self.accept)
        buttons_box.rejected.connect(self.reject)
        
        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Please enter your password")
        self.layout.addWidget(message)
        self.layout.addWidget(buttons_box)
        self.setLayout(self.layout)

class PasswordLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = ..., f: PySide6.QtCore.Qt.WindowFlags = ...) -> None:
        super().__init__()
        self.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setFixedSize(QtCore.QSize(300, 30))
        self.setPlaceholderText("Password")

class DevicesLayout(QtWidgets.QHBoxLayout):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = ..., f: PySide6.QtCore.Qt.WindowFlags = ...) -> None:
        super().__init__()
        self.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.setObjectName("DevicesLayout")

        self.devices_combobox = QtWidgets.QComboBox()
        self.devices_combobox.setMinimumSize(QtCore.QSize(100, 40))
        self.devices_combobox.addItems(get_dev_name())
        self.devices_combobox.setIconSize(QtCore.QSize(1, 1))

        horizontal_spacer0 = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Fixed)
        horizontal_spacer1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.MinimumExpanding)

        self.removable_checkbox = QtWidgets.QCheckBox("Show all")
        self.removable_checkbox.setMinimumSize(QtCore.QSize(0, 30))
        self.removable_checkbox.clicked.connect(self.show_removable_only)

        self.addWidget(self.devices_combobox)
        self.addItem(horizontal_spacer0)
        self.addWidget(self.removable_checkbox)
        self.addItem(horizontal_spacer1)
    
    def get_block_device_path(self) -> str:
        return self.devices_combobox.currentText()

    @QtCore.Slot()
    def show_removable_only(self):
        self.devices_combobox.clear()
        if self.removable_checkbox.isChecked():
            self.devices_combobox.addItems(get_dev_name(removable=False))
        else:
            self.devices_combobox.addItems(get_dev_name())

def cycle_generator(x):
    while True:
        for i in x:
            yield i

class PasswordLayout(QtWidgets.QVBoxLayout):
    def __init__(self,connected_widget:QtWidgets=None, parent: Optional[PySide6.QtWidgets.QWidget] = ..., f: PySide6.QtCore.Qt.WindowFlags = ...) -> None:
        super().__init__()
        self.connected_widget = connected_widget
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.setObjectName("PasswordLayout")

        self.password_line_edit = PasswordLineEdit()
        self.password_line_edit_retry = PasswordLineEdit()
        self.password_line_edit.textChanged.connect(self.check_password)
        self.password_line_edit_retry.textChanged.connect(self.check_password)
        self.addWidget(self.password_line_edit)
        self.addWidget(self.password_line_edit_retry)

    def get_password(self):
        if self.check_password():
            return self.password_line_edit.text()
    def check_password(self):
        if self.password_line_edit.text() == "" or self.password_line_edit_retry.text() == "":
            if self.connected_widget:
                self.connected_widget.setEnabled(False)
            return False
        elif self.password_line_edit.text() == self.password_line_edit_retry.text():
            if self.connected_widget:
                self.connected_widget.setEnabled(True)
            return True
        else:
            if self.connected_widget:
                self.connected_widget.setEnabled(False)
            return False

        
class CreatorWidget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = ..., f: PySide6.QtCore.Qt.WindowFlags = ...) -> None:
        self.parent = parent
        super().__init__()
        self.device_layout = DevicesLayout()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFixedSize(QtCore.QSize(420, 125))
        button = QtWidgets.QPushButton("Create\nSafeBox", self)
        button.setMinimumSize(QtCore.QSize(0, 110))
        button.setEnabled(False)
        button.clicked.connect(self.create_safebox)
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.setObjectName("right_layout")
        right_layout.addWidget(button)

        self.password_layout = PasswordLayout(button)
        
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.setObjectName("left_layout")
        left_layout.addLayout(self.device_layout)
        left_layout.addLayout(self.password_layout)

        layout = QtWidgets.QHBoxLayout()
        layout.setObjectName("layout")
        self.setLayout(layout)
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        print(self.size())


    @QtCore.Slot()
    def create_safebox(self):
        if self.password_layout.check_password():
            p = self.password_layout.get_password()
            print(p)
            safebox = SafeBox(self.device_layout.get_block_device_path(), p)
            
            print("Password is correct")
            answer = QtWidgets.QMessageBox.warning(self, "Wipe", "This action will erase all data on the device.\n"
                                                   "Are you sure you want to continue?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            
            if answer == QtWidgets.QMessageBox.Yes:
                safebox.create()
        else:
           print("Password is incorrect")
           QtWidgets.QMessageBox.warning(self, "Error", "Password is incorrect")