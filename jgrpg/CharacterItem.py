from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem


class CharacterItem(QStandardItem):

    def __init__(self, character):
        super(CharacterItem, self).__init__()
        self.setEditable(False)

        self.character = character
        self.setData(self.character, Qt.UserRole)
        self.character.changed.connect(self.on_change)
        self.on_change()

    def on_change(self):
        self.setData(self.character.name, Qt.DisplayRole)
