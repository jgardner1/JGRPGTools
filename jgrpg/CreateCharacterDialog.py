from PyQt5.uic import loadUiType

ui_CreateCharacterDialog, CreateCharacterDialogBaseClass = loadUiType('ui/CreateCharacterDialog.ui')

class CreateCharacterDialog(
        CreateCharacterDialogBaseClass,
        ui_CreateCharacterDialog
):
    
    def __init__(self):
        super(CreateCharacterDialog, self).__init__()

        self.setupUi(self)

    def accept(self):

        super(CreateCharacterDialog, self).accept()
