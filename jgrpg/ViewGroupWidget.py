from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/ViewGroupWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from jgrpg.model import Groups

import __main__


class ViewGroupWidget(base, ui):
    
    def __init__(self, *, obj):
        super(ViewGroupWidget, self).__init__()

        self.obj = obj

        # Setup the UI elements
        self.setupUi(self)

        obj.changed.connect(self.set_data)

        self.set_data()

    def set_data(self):
        group = self.obj

        self.setWindowTitle("{} (Group)".format(group.name))
        self.nameValueLabel.setText(group.name)


    def on_edit_clicked(self):
        mw = __main__.main_window
        window = mw.editObject(self.obj)
