from PyQt5.uic import loadUiType

ui_MainWindow, MainWindowBaseClass = loadUiType('ui/MainWindow.ui')

from jgrpg.CreateCharacterDialog import CreateCharacterDialog

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QCoreApplication

from jgrpg.model import Universe

class MainWindow(MainWindowBaseClass, ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.universe = None
        self.filename = None

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
        has_universe = self.universe != None

        self.actionSaveUniverse.setEnabled(has_universe)
        self.actionSaveUniverseAs.setEnabled(has_universe)
        self.menuCharacter.setEnabled(has_universe)


    def newUniverse(self):
        print("newUniverse")
        
        self.universe = Universe.new()
        self.filename = None

        self.activateActions()

    def openUniverse(self):
        print("openUniverse")

        filename, filefilter = QFileDialog.getOpenFileName(
            self,
            "Open Universe",
            filter="JGRPG Universe Files (*.jgu)")

        if not filename:
            return

        self.filename = filename
        self.universe = Universe.load_from_json(filename)
        self.activateActions()
        
    def saveUniverse(self):
        print("saveUniverse")
        if not self.filename:
            return self.saveUniverseAs()
        
    def saveUniverseAs(self):
        print("saveUniverseAs")
        filename, filefilter = QFileDialog.getSaveFileName(
            self,
            "Save Universe As",
            filter="JGRPG Universe Files (*.jgu)",
            options=QFileDialog.DontConfirmOverwrite)
        if not filename:
            return
        
        if not filename.endswith('.jgu'):
            filename += '.jgu'

        self.filename = filename
        self.universe.save_to_json(filename)

        self.activateActions()
