from PyQt5.uic import loadUiType

ui_CreateRaceDialog, CreateRaceDialogBaseClass = loadUiType('ui/CreateRaceDialog.ui')

from jgrpg.model import GlobalData

class CreateRaceDialog(
        CreateRaceDialogBaseClass,
        ui_CreateRaceDialog
):
    
    def __init__(self):
        super(CreateRaceDialog, self).__init__()

        self.setupUi(self)

    def accept(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
        }
        GlobalData.createRace(**data)

        super(CreateRaceDialog, self).accept()
