from PyQt5.uic import loadUiType

ui_CreateCharacterDialog, CreateCharacterDialogBaseClass = loadUiType('ui/CreateCharacterDialog.ui')

from PyQt5.QtCore import pyqtSignal
from jgrpg.model import GlobalData

from random import gauss, uniform

attributes = (
    'strength',
    'dexterity',
    'constitution',
    'intelligence',
    'wisdom',
    'charisma',
)

def attribute_roll():
    return uniform(-2,+2) + uniform(-2,+2) + uniform(-2,+2)
    

class CreateCharacterDialog(
        CreateCharacterDialogBaseClass,
        ui_CreateCharacterDialog
):

    attributeChanged = pyqtSignal('QString', int)
    
    def __init__(self):
        super(CreateCharacterDialog, self).__init__()

        self.setupUi(self)
        self.attributeChanged.connect(self.updateAttribute)

    def show(self):
        super(CreateCharacterDialog, self).show()

        # clear the attributes
        self.attr = dict()

        # Reroll all of them
        self.rerollAll()

    def rerollAll(self):
        for attr in attributes:
            self.reroll(attr)

    def rerollStrength(self):       self.reroll('strength')
    def rerollDexterity(self):      self.reroll('dexterity')
    def rerollConstitution(self):   self.reroll('constitution')
    def rerollIntelligence(self):   self.reroll('intelligence')
    def rerollWisdom(self):         self.reroll('wisdom')
    def rerollCharisma(self):       self.reroll('charisma')

    def reroll(self, attr):
        self.attr[attr] = attribute_roll()
        self.attributeChanged.emit(attr, self.attr[attr])

    def updateAttribute(self, attr, value):
        getattr(self, attr+'ValueLabel') \
            .setText("{:+0.1f}".format(self.attr[attr]))

    def accept(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
        }
        GlobalData.createCharacter(**data)

        super(CreateCharacterDialog, self).accept()
