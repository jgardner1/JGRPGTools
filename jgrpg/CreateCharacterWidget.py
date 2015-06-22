from PyQt5.uic import loadUiType

ui_CreateCharacterWidget, CreateCharacterWidgetBaseClass = loadUiType('ui/CreateCharacterWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMessageBox
from jgrpg.model import GlobalData
from jgrpg.model.attributes import attributes

from random import gauss, uniform, choice
from math import sqrt

from collections import defaultdict

def attribute_roll():
    return uniform(-2,+2) + uniform(-2,+2) + uniform(-2,+2)

class CreateCharacterWidget(
        CreateCharacterWidgetBaseClass,
        ui_CreateCharacterWidget
):


    rollChanged = pyqtSignal('QString')
    raceChanged = pyqtSignal()

    attributeChanged = pyqtSignal('QString')
    
    def __init__(self, race=None):
        super(CreateCharacterWidget, self).__init__()

        # initialize the attributes
        # attr['strength']['racial_modifier'] = 1.0
        #      ^ attribute  ^
        #                   + total, roll, racial_modifier
        self.attr = defaultdict(lambda: defaultdict(lambda: 0.0))
        self.race = None
        self.height_variance = 0.0
        self.weight_variance = 0.0

        # Setup the UI elements
        self.setupUi(self)

        # Signals
        self.rollChanged.connect(self.recalculate_attribute)
        self.raceChanged.connect(self.recalculate_attributes)
        self.raceChanged.connect(self.recalculate_size)
        self.attributeChanged.connect(self.label_attribute)
        self.attributeChanged.connect(self.recalculate_size_for_attribute_changed)

        self.selectRaceComboBox.currentIndexChanged.connect(self.selectRaceComboBox_onchange)
        self.selectRaceComboBox_onchange(self.selectRaceComboBox.currentIndex())

        self.genderButtonGroup.setId(self.maleRadioButton, 1)
        self.genderButtonGroup.setId(self.femaleRadioButton, 2)

        if race:
            self.selectRaceComboBox.setRace(race)

        # Reroll all of them
        self.rerollAll()


    def selectRaceComboBox_onchange(self, index):
        new_race = self.selectRaceComboBox.race()
        
        if self.race is new_race:
            return

        if self.race:
            self.race.changed.disconnect(self.on_race_changed)

        # Remember the race
        self.race = new_race
        self.race.changed.connect(self.on_race_changed)

        self.on_race_changed()

    def on_race_changed(self):
        # Enable the button for name generation if there are names
        if self.race is not None:
            self.randomNamePushButton.setEnabled(True)

        for attr in attributes:
            self.attr[attr]['racial_modifier'] = \
                self.race.attribute_modifiers.get(attr, 0.0)

        self.raceChanged.emit()

    def recalculate_attributes(self):
        for attr in attributes:
            self.recalculate_attribute(attr)

    def recalculate_attribute(self, attr):
        self.attr[attr]['total'] = \
            self.attr[attr]['roll'] \
            + self.attr[attr]['racial_modifier'] \

        self.attributeChanged.emit(attr)

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
        self.attr[attr]['roll'] = attribute_roll()
        self.rollChanged.emit(attr)

    def label_attribute(self, attr):
        label = getattr(self, attr+'ValueLabel')
        label.setText("{:+0.1f}".format(self.attr[attr]['total']))
        label.setToolTip("<b>{:+0.1f}</b> rolled<br/><b>{:+0.1f}</b> racial modifier".format(
            self.attr[attr]['roll'],
            self.attr[attr]['racial_modifier']))


    def accept(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
        }
        GlobalData.createCharacter(**data)

        self.parent().close()

    def reject(self):
        self.parent().close()

    def clicked(self, button):
        pass

    def randomizeSize(self):
        self.heightSlider.setValue(0)
        self.weightSlider.setValue(0)


    def setHeight(self, height):
        self.height_variance = height/100.0
        self.recalculate_size()

    def setWeight(self, weight):
        self.weight_variance = weight/100.0
        self.recalculate_size()

    def recalculate_size_for_attribute_changed(self, attr):
        if attr in ('strength', 'dexterity'):
            self.recalculate_size()

    def recalculate_size(self):
        attr_mod = pow(
                sqrt(4./3.),
                (self.attr['strength']['total']
                - self.attr['dexterity']['total'])/4.0)

        height = (self.race.height[0]
                + self.race.height[1]*self.height_variance
            )

        height_factor = height / self.race.height[0]

        weight = (self.race.weight[0]
                + self.race.weight[1]*self.weight_variance)*height_factor*attr_mod

        self.sizeValueLabel.setText("{:0.0f}' {:0.0f}\", {:0.0f} lbs".format(
            height//12, height%12,
            int(weight+0.5)))

        self.sizeValueLabel.setToolTip("""
            height factor: {:+0.2f}<br/>
            race avg. height: {}"<br/>
            race height var.: {}"<br/>
            height var. factror: {:+0.2f}<br/>
            attribute modifier: {:0.2f}<br/>
            weight factor: {:+0.2f}<br/>
            race avg. weight: {} lbs.<br/>
            race weight var.: {} lbs.
        """.format(
            attr_mod,
            self.height_variance,
            self.race.height[0],
            self.race.height[1],
            height_factor,
            self.weight_variance,
            self.race.weight[0],
            self.race.weight[1],
        ))
