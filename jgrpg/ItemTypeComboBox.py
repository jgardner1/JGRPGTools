from PyQt5.QtWidgets import QComboBox

from jgrpg.model import ItemPrototypes

class ItemTypeComboBox(QComboBox):

    def __init__(self, parent=None):
        super(ItemTypeComboBox, self).__init__(parent)

        self.setInsertPolicy(self.InsertAlphabetically)

        ItemPrototypes.added.connect(self.reset)
        ItemPrototypes.removed.connect(self.reset)
        ItemPrototypes.reset.connect(self.reset)


        self.reset()

        self.setEditable(True)


    def reset(self):
        unique_types = set([_.type for _ in ItemPrototypes])
        unique_types.add('misc')

        # Add items that are not in the list
        for t in unique_types:
            self.addItem(t)

        # Remove items that are no longer in the list
        for i in reversed(range(self.count())):
            if self.itemText(i) not in unique_types:
                self.removeItem(i)

        self.view().model().sort(0)
