from PyQt5.QtWidgets import QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from jgrpg.model import GlobalData

class UniverseTreeView(QTreeView):

    def __init__(self, parent=None):
        super(UniverseTreeView, self).__init__(parent)

        self.setModel(QStandardItemModel())

        self.init()

        GlobalData.character_added.connect(self.init)
        GlobalData.character_removed.connect(self.init)
        GlobalData.characters_reset.connect(self.init)


    def init(self):
        model = self.model()
        model.clear()

        root_item = model.invisibleRootItem()

        item = QStandardItem("Characters")
        root_item.appendRow(item)
        for _ in GlobalData.characters:
            item.appendRow(QStandardItem(_.name))
            
        item = QStandardItem("Races")
        root_item.appendRow(item)
        for _ in GlobalData.races:
            item.appendRow(QStandardItem(_.name))
            
