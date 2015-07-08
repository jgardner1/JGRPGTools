from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/GetItemDialog.ui')

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog


class GetItemDialog(base, ui):
    
    def __init__(self,
            title,          # The title of the dialog
            labelText,      # The label for the list of items
            createText,     # The text for the create button
            new_dialog_cls, # The class for the create dialog
            item_cls,       # The class for the item in the list
            model           # The data for the list of items
    ): 
        super(GetItemDialog, self).__init__()

        # Setup the UI elements
        self.setupUi(self)

        self.setWindowTitle(title)
        self.label.setText(labelText)
        self.createButton.setText(createText)
        self.new_dialog_cls = new_dialog_cls
        self.item_cls = item_cls
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

    def on_create_clicked(self):
        class _widget(self.new_dialog_cls):

            def on_accepted(self, button):
                role = self.buttonBox.buttonRole(button)
                if role == self.buttonBox.ApplyRole:
                    self.apply()
                elif role == self.buttonBox.ResetRole:
                    self.reset()
                elif role == self.buttonBox.AcceptRole:
                    self.apply()
                    self.parent().accept()
                elif role == self.buttonBox.RejectRole:
                    self.parent().reject()
                else:
                    print("Unknown role")


        class CreateDialog(QDialog):

            def __init__(self):
                super(CreateDialog, self).__init__()

                self.widget = _widget()
                self.widget.setParent(self)

            def accept(self):
                self.result = self.widget.obj
                super(CreateDialog, self).accept()

        dialog = CreateDialog()

        if dialog.exec() == QDialog.Accepted:
            self.treeView.model().appendRow(self.item_cls(dialog.result))
