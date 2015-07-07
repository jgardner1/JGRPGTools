from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem


class GroupItem(QStandardItem):

    def __init__(self, group):
        super(GroupItem, self).__init__()
        self.setEditable(False)

        self.group = group
        self.setData(self.group, Qt.UserRole)
        self.group.changed.connect(self.on_change)
        self.on_change()

    def on_change(self):
        self.setData(self.group.name, Qt.DisplayRole)
