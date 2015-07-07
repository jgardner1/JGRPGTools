from PyQt5.uic import loadUiType

ui_MainWindow, MainWindowBaseClass = loadUiType('ui/MainWindow.ui')

from jgrpg.CreateCharacterWidget import CreateCharacterWidget
from jgrpg.CreateRaceWidget import CreateRaceWidget
from jgrpg.CreateItemPrototypeWidget import CreateItemPrototypeWidget
from jgrpg.CreateGroupWidget import CreateGroupWidget
from jgrpg.CreateAreaWidget import CreateAreaWidget

from jgrpg.ViewRaceWidget import ViewRaceWidget
from jgrpg.ViewItemPrototypeWidget import ViewItemPrototypeWidget
from jgrpg.ViewGroupWidget import ViewGroupWidget

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication

from jgrpg.model import (
        File,
        Races, Characters, ItemPrototypes, Groups, Areas,
)


class MainWindow(MainWindowBaseClass, ui_MainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.file = File()

        self.dialogs = {}

    def create(self, cls):
        if cls is Characters.cls:
            return self.createCharacter()

        elif cls is Races.cls:
            return self.createRace()

        elif cls is ItemPrototypes.cls:
            return self.createItemPrototype()

        elif cls is Groups.cls:
            return self.createGroup()

        elif cls is Areas.cls:
            return self.createArea()

        else:
            print("I don't know how to create {}".format(cls))

    def createCharacter(self, race=None):
        window = self.mdiArea.addSubWindow(CreateCharacterWidget(race=race))
        window.show()
        return window

    def createRace(self):
        window = self.mdiArea.addSubWindow(CreateRaceWidget())
        window.setWindowTitle("Create Race")
        window.show()
        return window

    def createItemPrototype(self):
        window = self.mdiArea.addSubWindow(CreateItemPrototypeWidget())
        window.show()
        return window

    def createGroup(self):
        window = self.mdiArea.addSubWindow(CreateGroupWidget())
        window.show()
        return window

    def createArea(self):
        window = self.mdiArea.addSubWindow(CreateAreaWidget())
        window.show()
        return window

    def editObject(self, obj):
        """Edits an unknown object to the mdiArea."""
        widget_class = None
        if isinstance(obj, Races.cls):
            widget_class = CreateRaceWidget

        elif isinstance(obj, ItemPrototypes.cls):
            widget_class = CreateItemPrototypeWidget

        elif isinstance(obj, Groups.cls):
            widget_class = CreateGroupWidget

        elif isinstance(obj, Characters.cls):
            widget_class = CreateCharacterWidget

        elif isinstance(obj, Areas.cls):
            widget_class = CreateAreaWidget

        else:
            print("none of the above")

        if not widget_class:
            return

        self._open_or_surface_window(widget_class, obj=obj)



    def viewObject(self, obj):
        """Shows an unknown object to the mdiArea."""

        widget_class = None
        if isinstance(obj, Races.cls):
            widget_class = ViewRaceWidget

        elif isinstance(obj, ItemPrototypes.cls):
            widget_class = ViewItemPrototypeWidget

        elif isinstance(obj, Groups.cls):
            widget_class = ViewGroupWidget

        elif isinstance(obj, Characters.cls):
            widget_class = ViewCharacterWidget

        elif isinstance(obj, Areas.cls):
            widget_class = ViewAreaWidget

        else:
            print("none of the above")

        if not widget_class:
            return

        self._open_or_surface_window(widget_class, obj)


    def _open_or_surface_window(self, widget_class, obj):
        for window in self.mdiArea.subWindowList():
            widget = window.widget()
            if isinstance(widget, widget_class) and widget.obj is obj:
                self.mdiArea.setActiveSubWindow(window)
                break
        else:
            print("widget_class={}".format(widget_class))
            window = self.mdiArea.addSubWindow(widget_class(obj=obj))
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

        if isinstance(obj, Races.cls):
            Races.remove(obj)

        elif isinstance(obj, ItemPrototypes.cls):
            ItemPrototypes.remove(obj)

        elif isinstance(obj, Groups.cls):
            Groups.remove(obj)

        elif isinstance(obj, Characters.cls):
            Characters.remove(obj)

        elif isinstance(obj, Areas.cls):
            Areas.remove(obj)

        else:
            print("none of the above")


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
        self.file.new()

    def openUniverse(self):
        filename, filefilter = QFileDialog.getOpenFileName(
            self,
            "Open Universe",
            filter="JGRPG Universe Files (*.jgu)")

        if not filename:
            return

        self.file.open(filename)
        
    def saveUniverse(self):
        if not self.file.filename:
            return self.saveUniverseAs()

        self.file.save()
        
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

        self.file.save(filename)
