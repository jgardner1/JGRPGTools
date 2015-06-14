from PyQt5.uic import loadUiType

ui_CreatePersonalityDialog, CreatePersonalityDialogBaseClass = loadUiType('ui/CreatePersonalityDialog.ui')

from jgrpg.model import GlobalData
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class CreatePersonalityDialog(
        CreatePersonalityDialogBaseClass,
        ui_CreatePersonalityDialog
):
    
    def __init__(self):
        super(CreatePersonalityDialog, self).__init__()

        self.setupUi(self)

    def accept(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
        }
        GlobalData.createPersonality(**data)

        super(CreatePersonalityDialog, self).accept()
