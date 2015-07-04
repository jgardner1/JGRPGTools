from .ObjectStore import ObjectStore, ObjectStoreObject
from .Character import Characters

class Group(ObjectStoreObject):
    def update(self, *,
            id=None,
            name="Unnamed Group",
            characters=[]
    ):
        self.characters = [
            c if isinstance(c, Characters.cls) else Characters[c]
            for c in characters
        ]

        super(Group, self).update(id=id, name=name)


    def data(self):
        data = super(Group, self).data()

        data.update({
            'characters':[c.id for c in self.characters],
        })

        return data

Groups = ObjectStore(Group)
