from PyQt5.QtCore import QObject, pyqtSignal
from .ObjectStore import ObjectStore

class ItemPrototype(QObject):
    changed = pyqtSignal()
    deleted = pyqtSignal()

    def __init__(self, **data):
        super(ItemPrototype, self).__init__()
        self.update(**data)

    def update(self, *,
            name="Unnamed Item",
            type='misc',
            size=1.0,   # in
            weight=0.1, # lbs
            value=0.1  # gp
    ):
        self.name = name
        self.type = type
        self.size = float(size)
        self.weight = float(weight)
        self.value = float(value)

        # TODO: Damage, armor value, etc... for different classes of items.

        self.changed.emit()

    def data(self):
        return {
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'weight': self.weight,
            'value': self.value,
        }

ItemPrototypes = ObjectStore(ItemPrototype)


class ItemInstance(QObject):
    changed = pyqtSignal()

    def __init__(self, **data):
        super(ItemInstance, self).__init__()

        self.update(**data)

    def update(self, *,
            prototype,
            name=None,
            quality=1.0
    ):
        # Not using weakref here on purpose
        self.prototype = prototype
        self.name = name
        self.quality = quality

        self.prototype.changed.connect(self.prototype_changed)
        self.changed.emit()

    def prototype_changed(self):
        self.changed.emit()
