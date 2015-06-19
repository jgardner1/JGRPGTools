from PyQt5.uic import loadUiType

ui_MainWindow, MainWindowBaseClass = loadUiType('ui/MainWindow.ui')

from jgrpg.CreateCharacterDialog import CreateCharacterDialog
from jgrpg.CreateRaceDialog import CreateRaceDialog
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


    def createCharacter(self):
        return self.modelessDialog(CreateCharacterDialog)

    def createRace(self):
        return self.modelessDialog(CreateRaceDialog)

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
