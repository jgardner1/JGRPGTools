from PyQt5.uic import loadUiType

ui_MainWindow, MainWindowBaseClass = loadUiType('ui/MainWindow.ui')

from jgrpg.CreateCharacterWidget import CreateCharacterWidget
from jgrpg.CreateRaceWidget import CreateRaceWidget
from jgrpg.CreateItemPrototypeWidget import CreateItemPrototypeWidget
from jgrpg.ViewRaceWidget import ViewRaceWidget
from jgrpg.CreateSkillDialog import CreateSkillDialog
from jgrpg.CreatePersonalityDialog import CreatePersonalityDialog

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication

from jgrpg.model import (
        GlobalData,
        Character, Race, Skill, Personality,
        ItemPrototypes,
        ObjectStore,
)


class MainWindow(MainWindowBaseClass, ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        self.dialogs = {}

    def create(self, cls):
        if cls is Character:
            return self.createCharacter()
        elif cls is Race:
            return self.createRace()
        elif cls is ItemPrototypes.cls:
            return self.createItemPrototype()
        else:
            print("I don't know how to create {}".format(cls))

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

    def createItemPrototype(self):
        window = self.mdiArea.addSubWindow(CreateItemPrototypeWidget())
        window.setWindowTitle("Create Item Prototype")
        window.show()
        return window

    def editObject(self, obj):
        """Edits an unknown object to the mdiArea."""
        if isinstance(obj, Race):
            self.editRace(obj)

        elif isinstance(obj, Character):
            print("character")
        elif isinstance(obj, Skill):
            print("skill")
        elif isinstance(obj, Personality):
            print("personality")
        else:
            print("none of the above")


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

    def viewObject(self, obj):
        """Shows an unknown object to the mdiArea."""
        if isinstance(obj, Race):
            self.viewRace(obj)

        elif isinstance(obj, Character):
            print("character")
        elif isinstance(obj, Skill):
            print("skill")
        elif isinstance(obj, Personality):
            print("personality")
        else:
            print("none of the above")

    def viewRace(self, race):
        for window in self.mdiArea.subWindowList():
            widget = window.widget()
            if isinstance(widget, ViewRaceWidget) and widget.race is race:
                self.mdiArea.setActiveSubWindow(window)
                break
        else:
            window = self.mdiArea.addSubWindow(ViewRaceWidget(race))
            window.show()

    def deleteObject(self, obj):
        mbox = QMessageBox(
            QMessageBox.Warning,
            "Confirm Delete",
            "Do you want to delete {} ({})?".format(obj.name, obj.__class__.__name__),
            QMessageBox.Yes | QMessageBox.Cancel)
        ret = mbox.exec_()
        if ret != QMessageBox.Yes:
            return

        if isinstance(obj, Race):
            self.deleteRace(obj)
        elif isinstance(obj, Character):
            print("character")
        elif isinstance(obj, Skill):
            print("skill")
        elif isinstance(obj, Personality):
            print("personality")
        else:
            print("none of the above")


    def deleteRace(self, race):
        GlobalData.deleteRace(race)


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
