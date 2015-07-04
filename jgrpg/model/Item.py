from PyQt5.QtCore import QObject, pyqtSignal
from .ObjectStore import ObjectStore, ObjectStoreObject

class ItemPrototype(ObjectStoreObject):
    def update(self, *,
            id=None,
            name="Unnamed Item",
            type='misc',
            size=1.0,   # in
            weight=0.1, # lbs
            value=0.1  # gp
    ):
        self.type = type
        self.size = float(size)
        self.weight = float(weight)
        self.value = float(value)

        # TODO: Damage, armor value, etc... for different classes of items.

        super(ItemPrototype, self).update(id=id, name=name)

    def data(self):
        data = super(ItemPrototype, self).data()
        data.update({
            'type': self.type,
            'size': self.size,
            'weight': self.weight,
            'value': self.value,
        })

        return data

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
