from PyQt5.QtCore import QObject, pyqtSignal

class ObjectStore(QObject):
    """An ObjectStore stores a set of objects. The objects must be unique."""
    added = pyqtSignal(object)
    removed = pyqtSignal(object)
    reset = pyqtSignal()

    def __init__(self, cls):
        super(ObjectStore, self).__init__()

        # The contents of this store.
        self.contents = set()

        # The class used to create new instances.
        self.cls = cls

    def __iter__(self):
        return iter(self.contents)

    def load(self, data_list):
        """Replaces the contents with the new contents."""

        # Clear everything out
        self.contents = set()

        # Add things in one at a time
        for data in data_list:
            self.contents.add(self.cls(**data))

                  
        # Signal that everything has changed
        self.reset.emit()

    def save(self):
        """Dump the data in the form of a dict that can be turned into
        JSON. This is used for saving the data."""
        return [o.data() for o in self.contents]

    def add(self, **data):
        """Adds an item to the contents"""
        o = self.cls(**data)
        self.contents.add(o)
        self.added.emit(o)

    def remove(self, o):
        """Removes an item."""
        self.contents.remove(o)
        self.removed.emit(o)
