from PyQt5.uic import loadUiType

ui_CreateSkillDialog, CreateSkillDialogBaseClass = loadUiType('ui/CreateSkillDialog.ui')

from jgrpg.model import GlobalData
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QErrorMessage

class CreateSkillDialog(
        CreateSkillDialogBaseClass,
        ui_CreateSkillDialog
):
    
    def __init__(self):
        super(CreateSkillDialog, self).__init__()

        self.setupUi(self)

    def show(self):
        self.nameLineEdit.clear()

        super(CreateSkillDialog, self).show()


    def accept(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
        }

        errors = []
        if not data['name']:
            errors.append("'name' must not be blank.")

        if errors:
            QErrorMessage.qtHandler().showMessage(
                "<p>There were some errors creating the skill.</p>"
                +"<ul><li>"+("</li><li>".join(errors))+"</li></ul>")
            


        else:
            GlobalData.createSkill(**data)

            super(CreateSkillDialog, self).accept()
