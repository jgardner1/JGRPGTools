from PyQt5.uic import loadUiType

ui_MainWindow, MainWindowBaseClass = loadUiType('ui/MainWindow.ui')

from jgrpg.CreateCharacterDialog import CreateCharacterDialog

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QCoreApplication

from jgrpg.model import GlobalData

class MainWindow(MainWindowBaseClass, ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.activateActions()


    def createCharacter(self):
        try:
            dialog = self.createCharacterDialog
        except AttributeError:
            dialog = self.createCharacterDialog = CreateCharacterDialog()

        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def activateActions(self):
        """Activate or deactivate actions based on the state of the universe
        and filename."""
        has_universe = GlobalData.universe != None

        self.actionSaveUniverse.setEnabled(has_universe)
        self.actionSaveUniverseAs.setEnabled(has_universe)
        self.menuCharacter.setEnabled(has_universe)


    def newUniverse(self):
        GlobalData.new()
        self.activateActions()

    def openUniverse(self):
        filename, filefilter = QFileDialog.getOpenFileName(
            self,
            "Open Universe",
            filter="JGRPG Universe Files (*.jgu)")

        if not filename:
            return

        GlobalData.open(filename)
        self.activateActions()
        
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
        self.activateActions()
