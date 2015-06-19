from PyQt5.uic import loadUiType

ui_MainWindow, MainWindowBaseClass = loadUiType('ui/MainWindow.ui')

from jgrpg.CreateCharacterWidget import CreateCharacterWidget
from jgrpg.CreateRaceWidget import CreateRaceWidget
from jgrpg.ViewRaceWidget import ViewRaceWidget
from jgrpg.CreateSkillDialog import CreateSkillDialog
from jgrpg.CreatePersonalityDialog import CreatePersonalityDialog

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QCoreApplication

from jgrpg.model import GlobalData

class MainWindow(MainWindowBaseClass, ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.dialogs = {}


    def createCharacter(self, race=None):
        window = self.mdiArea.addSubWindow(CreateCharacterWidget(race))
        window.setWindowTitle("Create Character")
        window.show()
        return window

    def createRace(self):
        window = self.mdiArea.addSubWindow(CreateRaceWidget())
        window.setWindowTitle("Create Race")
        window.show()
        return window

    def editRace(self, race):
        for window in self.mdiArea.subWindowList():
            widget = window.widget()
            if isinstance(widget, CreateRaceWidget) and widget.race is race:
                self.mdiArea.setActiveSubWindow(window)
                break
        else:
            window = self.mdiArea.addSubWindow(CreateRaceWidget(race))
            window.setWindowTitle("Edit Race")
            window.show()

    def viewRace(self, race):
        for window in self.mdiArea.subWindowList():
            widget = window.widget()
            if isinstance(widget, ViewRaceWidget) and widget.race is race:
                self.mdiArea.setActiveSubWindow(window)
                break
        else:
            window = self.mdiArea.addSubWindow(ViewRaceWidget(race))
            window.show()

    def createSkill(self):
        return self.modelessDialog(CreateSkillDialog)

    def createPersonality(self):
        return self.modelessDialog(CreatePersonalityDialog)

    def modelessDialog(self, DialogClass):
        name = DialogClass.__name__
        try:
            dialog = self.dialogs[name]
        except KeyError:
            dialog = self.dialogs[name] = DialogClass()

        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
        
        return dialog


    def newUniverse(self):
        GlobalData.new()

    def openUniverse(self):
        filename, filefilter = QFileDialog.getOpenFileName(
            self,
            "Open Universe",
            filter="JGRPG Universe Files (*.jgu)")

        if not filename:
            return

        GlobalData.open(filename)
        
    def saveUniverse(self):
        if not GlobalData.filename:
            return self.saveUniverseAs()

        GlobalData.save()
        
    def saveUniverseAs(self):
        filename, filefilter = QFileDialog.getSaveFileName(
            self,
            "Save Universe As",
            filter="JGRPG Universe Files (*.jgu)",
            options=QFileDialog.DontConfirmOverwrite)
        if not filename:
            return
        
        if not filename.endswith('.jgu'):
            filename += '.jgu'

        GlobalData.save(filename)
