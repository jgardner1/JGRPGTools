from PyQt5.uic import loadUiType

ui_CreateRaceWidget, CreateRaceWidgetBaseClass = loadUiType('ui/CreateRaceWidget.ui')

from jgrpg.model import GlobalData

class CreateRaceWidget(
        CreateRaceWidgetBaseClass,
        ui_CreateRaceWidget
):

    def __init__(self, *, obj=None):
        super(CreateRaceWidget, self).__init__()

        self.obj = obj

        self.setupUi(self)

        self.reset()

    def clicked(self, button):
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
        if self.obj:
            race = self.obj

            self.setWindowTitle("Edit {} (Race)".format(race.name))
            self.nameLineEdit.setText(race.name)
            self.maleNamesTextEdit.setPlainText("\n".join(race.male_names))
            self.femaleNamesTextEdit.setPlainText("\n".join(race.female_names))
            self.familyNamesTextEdit.setPlainText("\n".join(race.family_names))

            self.strengthSpinBox.setValue(race.attribute_modifiers.get('strength', 0.0))
            self.dexteritySpinBox.setValue(race.attribute_modifiers.get('dexterity', 0.0))
            self.constitutionSpinBox.setValue(race.attribute_modifiers.get('constitution', 0.0))
            self.intelligenceSpinBox.setValue(race.attribute_modifiers.get('intelligence', 0.0))
            self.wisdomSpinBox.setValue(race.attribute_modifiers.get('wisdom', 0.0))
            self.charismaSpinBox.setValue(race.attribute_modifiers.get('charisma', 0.0))
        else:
            self.setWindowTitle("Create Race")
            self.nameLineEdit.setText("")
            self.maleNamesTextEdit.setPlainText("")
            self.femaleNamesTextEdit.setPlainText("")
            self.familyNamesTextEdit.setPlainText("")

            self.strengthSpinBox.setValue(0.0)
            self.dexteritySpinBox.setValue(0.0)
            self.constitutionSpinBox.setValue(0.0)
            self.intelligenceSpinBox.setValue(0.0)
            self.wisdomSpinBox.setValue(0.0)
            self.charismaSpinBox.setValue(0.0)

    def apply(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
            "male_names":self.maleNamesTextEdit.toPlainText().strip().split(),
            "female_names":self.femaleNamesTextEdit.toPlainText().strip().split(),
            "family_names":self.familyNamesTextEdit.toPlainText().strip().split(),
            "attribute_modifiers":{
                    "strength":self.strengthSpinBox.value(),
                    "dexterity":self.dexteritySpinBox.value(),
                    "constitution":self.constitutionSpinBox.value(),
                    "intelligence":self.intelligenceSpinBox.value(),
                    "wisdom":self.wisdomSpinBox.value(),
                    "charisma":self.charismaSpinBox.value(),
                },
        }
        if self.obj:
            self.obj.update(**data)
        else:
            self.obj = GlobalData.createRace(**data)
        self.reset()
