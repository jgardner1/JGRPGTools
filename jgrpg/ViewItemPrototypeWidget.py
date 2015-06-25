from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/ViewItemPrototypeWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from jgrpg.model import ItemPrototypes

import __main__


class ViewItemPrototypeWidget(base, ui):
    
    def __init__(self, item=None):
        super(ViewItemPrototypeWidget, self).__init__()

        self.obj = item

        # Setup the UI elements
        self.setupUi(self)

        item.changed.connect(self.set_data)

        self.set_data()

    def set_data(self):
        item = self.obj

        self.setWindowTitle("{} (Item Prototype)".format(item.name))
        self.nameValueLabel.setText(item.name)

    def createInstance(self):
        pass

    def copyPrototype(self):
        pass

    def editPrototype(self):
        mw = __main__.main_window
        window = mw.editObject(self.obj)
