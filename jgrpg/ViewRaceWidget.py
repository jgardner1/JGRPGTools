from PyQt5.uic import loadUiType

ui_ViewRaceWidget, ViewRaceWidgetBaseClass = loadUiType('ui/ViewRaceWidget.ui')

import __main__

class ViewRaceWidget(
        ViewRaceWidgetBaseClass,
        ui_ViewRaceWidget
):

    def __init__(self, race):
        super(ViewRaceWidget, self).__init__()

        self.race = race

        self.setupUi(self)

        self.set_data()

        race.removed.connect(self.removed)
        race.changed.connect(self.set_data)

    def set_data(self):
        race = self.race

        self.setWindowTitle(race.name+" (Race)")
        self.nameValueLabel.setText(race.name)
        self.maleNamesValueLabel.setText(", ".join(race.male_names))
        self.femaleNamesValueLabel.setText(", ".join(race.female_names))
        self.familyNamesValueLabel.setText(", ".join(race.family_names))

    def removed(self):
        self.parent().close()
        

    def createCharacter(self):
        print("Create character")
        mw = __main__.main_window
        mw.createCharacter(self.race)
        
    def copyRace(self):
        print("Copy race")
        
    def editRace(self):
        mw = __main__.main_window
        window = mw.editRace(self.race)

