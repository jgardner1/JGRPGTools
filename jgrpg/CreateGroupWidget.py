from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/CreateGroupWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from jgrpg.model import Groups


class CreateGroupWidget(base, ui):
    
    def __init__(self, group=None):
        """Creates an populates a Create / Edit Group Window.

        If group is specified, it is an edit window.
        """
        super(CreateGroupWidget, self).__init__()

        self.obj = group

        # Setup the UI elements
        self.setupUi(self)

        self.reset()

    def on_accepted(self, button):
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
            # Reset to the original group
            group = self.obj

            # Set the window title
            self.setWindowTitle("Edit {} (Group)".format(group.name))

            # Set the name line edit
            self.nameLineEdit.setText(group.name)


        else:
            # Set the defaults
            self.setWindowTitle("Create Group")
            self.nameLineEdit.setText("")

    def apply(self):
        # Create or update the item.
        data = {
            "name":self.nameLineEdit.text().strip(),
        }
        if self.obj:
            # Update the item because we are editing it
            self.obj.update(**data)
        else:
            # Create the item because we are creating a new one
            self.obj = Groups.add(**data)
        self.reset()

    def on_add_character(self):
        pass
