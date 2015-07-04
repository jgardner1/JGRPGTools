from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/CreateGroupWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QDialog
from jgrpg.model import Groups, Characters
from jgrpg.GetItemDialog import GetItemDialog
from jgrpg.CharacterItem import CharacterItem


class CreateGroupWidget(base, ui):
    
    def __init__(self, *, obj=None):
        """Creates an populates a Create / Edit Group Window.

        If group is specified, it is an edit window.
        """
        super(CreateGroupWidget, self).__init__()

        self.obj = obj

        # Setup the UI elements
        self.setupUi(self)

        self.reset()

        # NOTE: disable the "add character" button if there are no characters
        # left to add.


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
        # Either way, we are going to replace the model.
        model = QStandardItemModel()
        self.charactersListView.setModel(model)

        if self.obj:
            # Reset to the original group
            group = self.obj

            # Set the window title
            self.setWindowTitle("Edit {} (Group)".format(group.name))

            # Set the name line edit
            self.nameLineEdit.setText(group.name)

            for c in group.characters:
                model.appendRow(CharacterItem(c))

        else:
            # Set the defaults
            self.setWindowTitle("Create Group")
            self.nameLineEdit.setText("")


    def apply(self):
        model = self.charactersListView.model()

        # Create or update the item.
        data = {
            "name":self.nameLineEdit.text().strip(),
            "characters":[
                model.data(model.index(i,0), Qt.UserRole)
                for i in range(model.rowCount())
            ],
        }
        if self.obj:
            # Update the item because we are editing it
            self.obj.update(**data)
        else:
            # Create the item because we are creating a new one
            self.obj = Groups.add(**data)
        self.reset()


    def on_add_character(self):
        """
        Create a popup dialog that has a single list view of all the
        characters that are not yet added. 
        """

        # figure out who is added.
        characters_added = set()
        model = self.charactersListView.model()
        for i in range(model.rowCount()):
            characters_added.add(model.data(model.index(i, 0), Qt.UserRole))
            

        model = QStandardItemModel()
        for c in Characters:
            if c in characters_added: continue

            model.appendRow(CharacterItem(c))

        dialog = GetItemDialog("Choose a Character to Add",
            "Characters",
            model
        )

        if dialog.exec() == QDialog.Accepted:
            model = self.charactersListView.model()
            model.appendRow(CharacterItem(dialog.selection))
