from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/GetItemDialog.ui')


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog


class GetItemDialog(base, ui):
    
    def __init__(self, title, labelText, model):
        super(GetItemDialog, self).__init__()

        # Setup the UI elements
        self.setupUi(self)


        self.setWindowTitle(title)
        self.label.setText(labelText)
        self.treeView.setModel(model)

        self.treeView.activated.connect(self.on_activated)

        self.selection = None

    def on_activated(self, index):
        print("on_activated")
        self.selection = index.data(Qt.UserRole)
        self.accept()

    def current_changed(self, current, previous):
        print("current_changed")
        self.selection = current.data(Qt.UserRole)



