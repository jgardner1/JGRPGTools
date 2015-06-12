#!/usr/bin/env python3

import sys

from PyQt5.uic import loadUiType

ui_MainWindow, MainWindowBaseClass = loadUiType('ui/MainWindow.ui')
ui_CreateCharacterDialog, CreateCharacterDialogBaseClass = loadUiType('ui/CreateCharacterDialog.ui')

from PyQt5.Qt import Qt

from PyQt5.QtWidgets import (
        QApplication,
        QWidget,
        QMainWindow,
        QMdiArea,
        QMdiSubWindow,
        QTextEdit,
        QVBoxLayout,
        QHBoxLayout,
        QPushButton,
        QLineEdit,
)
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl

class CreateCharacterDialog(
        CreateCharacterDialogBaseClass,
        ui_CreateCharacterDialog
):
    
    def __init__(self):
        super(CreateCharacterDialog, self).__init__()

        self.setupUi(self)


class MainWindow(MainWindowBaseClass, ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

    def createCharacter(self):
        try:
            dialog = self.createCharacterDialog
        except AttributeError:
            dialog = self.createCharacterDialog = CreateCharacterDialog()
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    app.exec()
