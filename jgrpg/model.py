import json
from weakref import proxy

class Universe(object):
    """The Universe stores all the things in the universe. It is like the
    database instance."""

    def __init__(self, *, characters=[]):
        self.characters = [Character(self, **c) for c in characters]

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
    """A character is any creature."""

    def __init__(self, universe, *, name=""):
        self.name = name

    def __json__(self):
        return {
            'name':self.name,
        }

class GlobalData(object):
    """Stores the global data available everywhere in the app."""
    universe = None
    filename = None

    @classmethod
    def open(cls, filename):
        cls.universe = Universe.load_from_json(filename)
        cls.filename = filename

    @classmethod
    def save(cls, filename=None):
        filename = filename or cls.filename
        cls.universe.save_to_json(filename)
        cls.filename = filename

    @classmethod
    def new(cls):
        cls.filename = None
        cls.universe = Universe.new()

    @classmethod
    def createCharacter(cls, **data):
        character = Character(cls.universe, **data)
        cls.universe.characters.append(character)
        return character

