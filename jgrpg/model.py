import json
from weakref import proxy

class Universe(object):
    """The Universe stores all the things in the universe. It is like the
    database instance."""

    def __init__(self, *, characters=[], races=[]):
        self.characters = [Character(self, **_) for _ in characters]
        self.races = [Race(self, **_) for _ in races]

    @classmethod
    def load_from_json(cls, f):
        data = json.load(open(f, 'r', encoding='utf8'))
        return cls(**data)

    def save_to_json(self, f):
        data = json.dump(self.__json__(), open(f, 'w', encoding='utf8'), indent=2)
        
    @classmethod
    def new(cls):
        # TODO: Default universe .jgu file
        return cls(**{
            "characters":[],
            "races":[],
        })

    def __json__(self):
        return {
            'characters':[_.__json__() for _ in self.characters],
            'races':[_.__json__() for _ in self.races],
        }

class Character(object):
    """A character is any creature."""

    def __init__(self, universe, *, name=""):
        self.name = name

    def __json__(self):
        return {
            'name':self.name,
        }

class Race(object):
    """A race is a type of creature."""

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

    @classmethod
    def createRace(cls, **data):
        race = Race(cls.universe, **data)
        cls.universe.races.append(race)
        return race

