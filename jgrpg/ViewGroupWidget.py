from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/ViewGroupWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel
from jgrpg.model import Groups
from jgrpg.CharacterItem import CharacterItem

import __main__


class ViewGroupWidget(base, ui):
    
    def __init__(self, *, obj):
        super(ViewGroupWidget, self).__init__()

        self.obj = obj

        # Setup the UI elements
        self.setupUi(self)

        obj.changed.connect(self.set_data)

        self.charactersListView.activated.connect(self.on_activated)

        self.set_data()

    def set_data(self):
        group = self.obj

        self.setWindowTitle("{} (Group)".format(group.name))
        self.nameValueLabel.setText(group.name)

        model = QStandardItemModel()
        self.charactersListView.setModel(model)
        for c in group.characters:
            item = CharacterItem(c)
            model.appendRow(item)


    def on_edit_clicked(self):
        mw = __main__.main_window
        window = mw.editObject(self.obj)

    def on_activated(self, index):
        character = index.data(Qt.UserRole)

        __main__.main_window.viewObject(character)


        
        
