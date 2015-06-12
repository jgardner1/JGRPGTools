import json


class Universe(object):

    def __init__(self, *, characters=[]):
        self.characters = [Character(**c) for c in characters]

    @classmethod
    def load_from_json(cls, f):
        data = json.load(open(f, 'r'))
        return cls(**data)

    @classmethod
    def new(cls):
        return cls(**{
            "characters":[],
        })

    def __json__(self):
        return {
            'characters':[c.__json__() for c in self.characters]
        }

    def save_to_json(self, f):
        data = json.dump(self.__json__(), open(f, 'w'))
        


class Character(object):

    def __init__(self, *, name=""):
        self.name = name

    def __json__(self):
        return {
            'name':self.name,
        }
