import json
from weakref import proxy

from PyQt5.QtGui import QStandardItemModel, QStandardItem

class Universe(QStandardItemModel):
    """The Universe stores all the things in the universe. It is like the
    database instance."""

    def __init__(self, **data):
        super(Universe, self).__init__()

        self.init_from_data(**data)

    def init_from_data(self, *, characters=[], races=[]):
        self.clear()

        root_item = self.invisibleRootItem()

        self.characters = QStandardItem("Characters")
        root_item.appendRow(self.characters)

        characters = [Character(self, **data) for data in characters]

        for _ in characters:
            self.characters.appendRow(_)

        self.races = QStandardItem("Races")
        root_item.appendRow(self.races)

        races = [Race(self, **data) for data in races]

        for _ in races:
            self.races.appendRow(_)


    def load_from_json(self, f):
        data = json.load(open(f, 'r', encoding='utf8'))
        self.init_from_data(**data)

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

class Character(QStandardItem):
    """A character is any creature."""

    def __init__(self, universe, *, name=""):
        super(Character, self).__init__(name)
        self.name = name

    def __json__(self):
        return {
            'name':self.name,
        }

class Race(QStandardItem):
    """A race is a type of creature."""

    def __init__(self, universe, *, name=""):
        super(Race, self).__init__(name)
        self.name = name

    def __json__(self):
        return {
            'name':self.name,
        }


class GlobalData(object):
    """Stores the global data available everywhere in the app."""
    universe = Universe.new()
    filename = None

    @classmethod
    def open(cls, filename):
        cls.universe.load_from_json(filename)
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

