from PyQt5.uic import loadUiType

ui_CreateCharacterDialog, CreateCharacterDialogBaseClass = loadUiType('ui/CreateCharacterDialog.ui')

from jgrpg.model import GlobalData

class CreateCharacterDialog(
        CreateCharacterDialogBaseClass,
        ui_CreateCharacterDialog
):
    
    def __init__(self):
        super(CreateCharacterDialog, self).__init__()

        self.setupUi(self)

    def accept(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
        }
        GlobalData.createCharacter(**data)

        super(CreateCharacterDialog, self).accept()
