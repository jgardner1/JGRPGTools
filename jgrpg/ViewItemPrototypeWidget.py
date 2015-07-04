from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/ViewItemPrototypeWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from jgrpg.model import ItemPrototypes

import __main__


class ViewItemPrototypeWidget(base, ui):
    
    def __init__(self, *, obj):
        super(ViewItemPrototypeWidget, self).__init__()

        self.obj = obj

        # Setup the UI elements
        self.setupUi(self)

        obj.changed.connect(self.set_data)

        self.set_data()

    def set_data(self):
        item = self.obj

        self.setWindowTitle("{} (Item Prototype)".format(item.name))
        self.nameValueLabel.setText(item.name)
        self.typeValueLabel.setText(item.type)
        self.weightValueLabel.setText(item.weight)
        self.sizeValueLabel.setText(item.size)
        self.valueValueLabel.setText(item.value)

    def createInstance(self):
        pass

    def copyPrototype(self):
        pass

    def editPrototype(self):
        mw = __main__.main_window
        window = mw.editObject(self.obj)
