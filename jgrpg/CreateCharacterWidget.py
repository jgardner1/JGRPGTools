from PyQt5.uic import loadUiType

ui_CreateCharacterWidget, CreateCharacterWidgetBaseClass = loadUiType('ui/CreateCharacterWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMessageBox
from jgrpg.model import GlobalData

from random import gauss, uniform, choice

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
    

class CreateCharacterWidget(
        CreateCharacterWidgetBaseClass,
        ui_CreateCharacterWidget
):

    attributeChanged = pyqtSignal('QString', int)
    
    def __init__(self, race=None):
        super(CreateCharacterWidget, self).__init__()

        self.setupUi(self)
        self.attributeChanged.connect(self.updateAttribute)

        self.selectRaceComboBox.currentIndexChanged.connect(self.race_changed)
        self.race_changed(0)

        self.genderButtonGroup.setId(self.maleRadioButton, 1)
        self.genderButtonGroup.setId(self.femaleRadioButton, 2)

        if race:
            self.selectRaceComboBox.setRace(race)

        # clear the attributes
        self.attr = dict()

        # Reroll all of them
        self.rerollAll()


    def race_changed(self, index):
        print("race changed")
        if self.selectRaceComboBox.itemData(index, Qt.UserRole) is not None:
            self.randomNamePushButton.setEnabled(True)
        

    def randomizeName(self):
        race = self.selectRaceComboBox.currentData(Qt.UserRole)
        if not race:
            print("No race")
            return

        gender = self.genderButtonGroup.checkedId()

        name = race.generate_name(male=gender==1, female=gender==2)

        self.nameLineEdit.setText(name)

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

        self.parent().close()

    def reject(self):
        self.parent().close()




	
