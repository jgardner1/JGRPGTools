from PyQt5.uic import loadUiType

ui_CreateRaceWidget, CreateRaceWidgetBaseClass = loadUiType('ui/CreateRaceWidget.ui')

from jgrpg.model import GlobalData

class CreateRaceWidget(
        CreateRaceWidgetBaseClass,
        ui_CreateRaceWidget
):

    def __init__(self, race=None):
        super(CreateRaceWidget, self).__init__()

        self.race = race

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
        if self.race:
            race = self.race
            self.nameLineEdit.setText(race.name)
            self.maleNamesTextEdit.setPlainText("\n".join(race.male_names))
            self.femaleNamesTextEdit.setPlainText("\n".join(race.female_names))
            self.familyNamesTextEdit.setPlainText("\n".join(race.family_names))
        else:
            self.nameLineEdit.setText("")
            self.maleNamesTextEdit.setPlainText("")
            self.femaleNamesTextEdit.setPlainText("")
            self.familyNamesTextEdit.setPlainText("")

    def apply(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
            "male_names":self.maleNamesTextEdit.toPlainText().strip().split(),
            "female_names":self.femaleNamesTextEdit.toPlainText().strip().split(),
            "family_names":self.familyNamesTextEdit.toPlainText().strip().split(),
        }
        if self.race:
            self.race.update(**data)
        else:
            self.race = GlobalData.createRace(**data)
