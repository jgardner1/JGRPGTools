from PyQt5.uic import loadUiType

ui, base = loadUiType('ui/CreateItemPrototypeWidget.ui')

from PyQt5.QtCore import pyqtSignal, Qt
from jgrpg.model import GlobalData


class CreateItemPrototypeWidget(base, ui):
    
    def __init__(self, item=None):
        """Creates an populates a Create / Edit Item Window.

        If item is specified, it is an edit window."""
        super(CreateItemPrototypeWidget, self).__init__()

        self.item = item

        # Setup the UI elements
        self.setupUi(self)
