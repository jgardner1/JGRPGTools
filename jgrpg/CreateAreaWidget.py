from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/CreateAreaWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QDialog
from jgrpg.model import Areas, Groups
from jgrpg.GetItemDialog import GetItemDialog
from jgrpg.GroupItem import GroupItem

class CreateAreaWidget(base, ui):
    
    def __init__(self, *, obj=None):
        """Creates an populates a Create / Edit Area Window.

        If obj is specified, it is an edit window.
        """
        super(CreateAreaWidget, self).__init__()

        self.obj = obj

        # Setup the UI elements
        self.setupUi(self)

        self.reset()

        # NOTE: disable the "add group" button if there are no groups
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
        self.groupsListView.setModel(model)

        if self.obj:
            # Reset to the original area
            area = self.obj

            # Set the window title
            self.setWindowTitle("Edit {} (Area)".format(area.name))

            # Set the name line edit
            self.nameLineEdit.setText(area.name)

            for g in area.groups:
                model.appendRow(GroupItem(c))

        else:
            # Set the defaults
            self.setWindowTitle("Create Area")
            self.nameLineEdit.setText("")


    def apply(self):
        model = self.groupsListView.model()

        # Create or update the item.
        data = {
            "name":self.nameLineEdit.text().strip(),
            "groups":[
                model.data(model.index(i,0), Qt.UserRole)
                for i in range(model.rowCount())
            ],
        }
        if self.obj:
            # Update the item because we are editing it
            self.obj.update(**data)
        else:
            # Create the item because we are creating a new one
            self.obj = Areas.add(**data)
        self.reset()


    def on_add_group(self):
        """
        Create a popup dialog that has a single list view of all the
        groups that are not yet added. 
        """

        # figure out who is added.
        groups_added = set()
        model = self.groupsListView.model()
        for i in range(model.rowCount()):
            groups_added.add(model.data(model.index(i, 0), Qt.UserRole))
            

        # Add rows for each unadded group
        model = QStandardItemModel()
        for g in Groups:
            if g in groups_added: continue

            model.appendRow(GroupItem(g))

        dialog = GetItemDialog("Choose a Group to Add",
            "Groups",
            model
        )

        if dialog.exec() == QDialog.Accepted:
            model = self.groupsListView.model()
            model.appendRow(GroupItem(dialog.selection))

    def on_add_item(self):
        pass

    def on_add_exit(self):
        pass
