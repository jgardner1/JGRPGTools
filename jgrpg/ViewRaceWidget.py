from PyQt5.uic import loadUiType

ui_ViewRaceWidget, ViewRaceWidgetBaseClass = loadUiType('ui/ViewRaceWidget.ui')


class ViewRaceWidget(
        ViewRaceWidgetBaseClass,
        ui_ViewRaceWidget
):

    def __init__(self, race):
        super(ViewRaceWidget, self).__init__()

        self.race = race

        self.setupUi(self)

        print("Setting window title")
        self.setWindowTitle(race.name+" (Race)")

        print("Setting name text")
        self.nameValueLabel.setText(race.name)
