from .ObjectStore import ObjectStore, ObjectStoreObject
from .Character import Characters

class Area(ObjectStoreObject):
    def update(self, *,
            id=None,
            name="Unnamed Area",
            groups=[],
            items=[],
            exits={}
    ):
        self.groups = [
            g if isinstance(g, Groups.cls) else Groups[g]
            for g in groups
        ]

        self.items = [
            i if isinstance(i, Items.cls) else Items[i]
            for i in items
        ]

        # One day exits will be more than direction -> room. For now, a dict
        # is fine.
        self.exits = {
            n:a if isinstance(a, Areas.cls) else Areas[a]
            for n,a in exits.items()
        }

        super(Area, self).update(id=id, name=name)


    def data(self):
        data = super(Area, self).data()

        data.update({
            'groups':[g.id for g in self.groups],
            'items':[i.id for i in self.items],
            'exits':{n:a.id for n,a in exits.items()}
        })

        return data

Areas = ObjectStore(Area)
