from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

from jgrpg.model.weapon_types import weapon_types

class WeaponTypeComboBox(QComboBox):

    def __init__(self, parent=None):
        super(WeaponTypeComboBox, self).__init__(parent)

        self.setModel(QStandardItemModel())

        self.init()

    def init(self):
        model = self.model()
        model.clear()

        root_item = model.invisibleRootItem()
        for t in weapon_types:
            item = QStandardItem(t.title())
            item.setData(t, Qt.UserRole)
            root_item.appendRow(item)
            
    def setWeaponType(self, t):
        count = self.count()        
        for i in range(count):
            if self.itemData(i, Qt.UserRole) is t:
                self.setCurrentIndex(i)
                break
        else:
            print("Couldn't find that weapon type...")

    def weaponType(self):
        """Returns the currently selected weapon type."""
        return self.currentData(Qt.UserRole)
