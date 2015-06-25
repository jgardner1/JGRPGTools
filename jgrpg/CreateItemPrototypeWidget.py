from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/CreateItemPrototypeWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from jgrpg.model import ItemPrototypes


class CreateItemPrototypeWidget(base, ui):
    
    def __init__(self, item=None):
        """Creates an populates a Create / Edit Item Window.

        If item is specified, it is an edit window."""
        super(CreateItemPrototypeWidget, self).__init__()

        self.obj = item

        # Setup the UI elements
        self.setupUi(self)

        self.reset()

    def clicked(self, button):
        role = self.buttonBox.buttonRole(button)
        if role == self.buttonBox.ApplyRole:
            self.apply()
        elif role == self.buttonBox.ResetRole:
            self.reset()
        elif role == self.buttonBox.AcceptRole:
            self.apply()
            self.parent().close()
        elif role == self.buttonBox.RejectRole:
            self.parent().close()
        else:
            print("Unknown role")

    def reset(self):
        if self.obj:
            # Reset to the original item
            item = self.obj
            self.setWindowTitle("Edit {} (Item Prototype)".format(item.name))
            self.nameLineEdit.setText(item.name)

            type_index = self.typeComboBox.findText(item.type)
            if type_index == -1:
                self.typeComboBox.setEditText(item.type)
            else:
                self.typeComboBox.setCurrentIndex(type_index)
        else:
            # Set the defaults
            self.setWindowTitle("Create Item Prototype")
            self.nameLineEdit.setText("")
            self.typeComboBox.setCurrentIndex(-1)

    def apply(self):
        # Create or update the item.
        data = {
            "name":self.nameLineEdit.text().strip(),
            "type":self.typeComboBox.currentText().strip(),
        }
        if self.obj:
            # Update the item because we are editing it
            self.obj.update(**data)
        else:
            # Create the item because we are creating a new one
            self.obj = ItemPrototypes.add(**data)
        self.reset()
