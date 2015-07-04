from PyQt5.QtCore import QObject, pyqtSignal

from uuid import uuid4

class ObjectStoreObject(QObject):
    changed = pyqtSignal()
    deleted = pyqtSignal()

    def __init__(self, **data):
        super(ObjectStoreObject, self).__init__()
        self.update(**data)

    def update(self, *, id=None, name=None):
        if id is None:
            id = str(uuid4())
        self.id = id

        self.name = name

        self.changed.emit()

    def data(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
    

class ObjectStore(QObject):
    """An ObjectStore stores a set of objects. The objects must be unique."""
    added = pyqtSignal(object)
    removed = pyqtSignal(object)
    reset = pyqtSignal()

    def __init__(self, cls):
        super(ObjectStore, self).__init__()

        # The contents of this store.
        self.contents = dict()

        # The class used to create new instances.
        self.cls = cls

    def __iter__(self):
        return iter(self.contents.values())

    def __getitem__(self, id):
        return self.contents[id]
        

    def load(self, data_list):
        """Replaces the contents with the new contents."""

        # Clear everything out
        self.contents = dict()

        # Add things in one at a time
        for data in data_list:
            obj = self.cls(**data)
            self.contents[obj.id] = obj

                  
        # Signal that everything has changed
        self.reset.emit()

    def save(self):
        """Dump the data in the form of a dict that can be turned into
        JSON. This is used for saving the data."""
        return [o.data() for o in self.contents.values()]

    def add(self, **data):
        """Adds an item to the contents"""
        o = self.cls(**data)
        self.contents[o.id] = o
        self.added.emit(o)

        return o

    def remove(self, o):
        """Removes an item."""
        del self.contents[o.id]
        self.removed.emit(o)

        return o
