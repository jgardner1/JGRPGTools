from .ObjectStore import ObjectStore, ObjectStoreObject

class Character(ObjectStoreObject):

    def update(self, *,
            id=None,
            name="Unnamed Character"
    ):
        # Apply our updates here before calling super(). super() will call
        # changed.emit()
        super(Character, self).update(id=id, name=name)


    def data(self):
        data = super(Character, self).data()

        return data

Characters = ObjectStore(Character)
