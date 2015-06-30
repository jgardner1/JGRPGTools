from PyQt5.QtCore import QObject, pyqtSignal
from .ObjectStore import ObjectStore

class Group(QObject):
    changed = pyqtSignal()
    deleted = pyqtSignal()

    def __init__(self, **data):
        super(Group, self).__init__()
        self.update(**data)

    def update(self, *,
            name="Unnamed Group"
    ):
        self.name = name

        self.changed.emit()

    def data(self):
        return {
            'name': self.name,
        }

Groups = ObjectStore(Group)
