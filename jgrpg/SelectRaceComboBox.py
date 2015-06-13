from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from jgrpg.model import GlobalData

class SelectRaceComboBox(QComboBox):

    def __init__(self, parent=None):
        super(SelectRaceComboBox, self).__init__(parent)

        self.setModel(QStandardItemModel())

        self.init()

        GlobalData.race_added.connect(self.init)
        GlobalData.race_removed.connect(self.init)
        GlobalData.races_reset.connect(self.init)

    def init(self):
        print("SelectRaceComboBox.init")
        model = self.model()
        model.clear()

        root_item = model.invisibleRootItem()
        for _ in GlobalData.races:
            root_item.appendRow(QStandardItem(_.name))
