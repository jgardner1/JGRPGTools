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

        if race:
            self.nameLineEdit.setText(race.name)

    def accept(self):
        data = {
            "name":self.nameLineEdit.text().strip(),
        }
        if self.race:
            print("Updating a race")
            self.race.update(**data)
        else:
            print("Creating a new race")
            GlobalData.createRace(**data)
        print("accepted")
        self.parent().close()

    def reject(self):
        print("rejected")
        self.parent().close()
