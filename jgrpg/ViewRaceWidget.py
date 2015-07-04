from PyQt5.uic import loadUiType

ui_ViewRaceWidget, ViewRaceWidgetBaseClass = loadUiType('ui/ViewRaceWidget.ui')

import __main__

class ViewRaceWidget(
        ViewRaceWidgetBaseClass,
        ui_ViewRaceWidget
):

    def __init__(self, *, obj):
        super(ViewRaceWidget, self).__init__()

        self.obj = obj

        self.setupUi(self)

        self.set_data()

        obj.removed.connect(self.removed)
        obj.changed.connect(self.set_data)

    def set_data(self):
        race = self.obj

        self.setWindowTitle(race.name+" (Race)")
        self.nameValueLabel.setText(race.name)
        self.maleNamesValueLabel.setText(", ".join(race.male_names))
        self.femaleNamesValueLabel.setText(", ".join(race.female_names))
        self.familyNamesValueLabel.setText(", ".join(race.family_names))

        self.strengthValueLabel.setText("{:+0.1f}".format(race.attribute_modifiers.get('strength', 0.0)))
        self.dexterityValueLabel.setText("{:+0.1f}".format(race.attribute_modifiers.get('dexterity', 0.0)))
        self.constitutionValueLabel.setText("{:+0.1f}".format(race.attribute_modifiers.get('constitution', 0.0)))
        self.intelligenceValueLabel.setText("{:+0.1f}".format(race.attribute_modifiers.get('intelligence', 0.0)))
        self.wisdomValueLabel.setText("{:+0.1f}".format(race.attribute_modifiers.get('wisdom', 0.0)))
        self.charismaValueLabel.setText("{:+0.1f}".format(race.attribute_modifiers.get('charisma', 0.0)))

    def removed(self):
        self.parent().close()
        

    def createCharacter(self):
        print("Create character")
        mw = __main__.main_window
        mw.createCharacter(self.obj)
        
    def copyRace(self):
        print("Copy race")
        
    def editRace(self):
        mw = __main__.main_window
        window = mw.editObject(self.obj)

