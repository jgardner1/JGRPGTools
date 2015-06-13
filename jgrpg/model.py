import json
from weakref import proxy

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class Universe(QObject):
    """The Universe stores all the things in the universe. It is like the
    database instance."""

    def __init__(self, **data):
        super(Universe, self).__init__()
        self.characters = []
        self.races = []

        self.init_from_data(**data)

    def init_from_data(self, *, characters=[], races=[]):
        self.characters[:] = [Character(self, **data) for data in characters]
        self.races[:] = [Race(self, **data) for data in races]

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

class Character(QObject):
    """A character is any creature."""

    def __init__(self, universe, *, name=""):
        super(Character, self).__init__()
        self.name = name

    def __json__(self):
        return {
            'name':self.name,
        }

class Race(QObject):
    """A race is a type of creature."""

    def __init__(self, universe, *, name=""):
        super(Race, self).__init__()
        self.name = name

    def __json__(self):
        return {
            'name':self.name,
        }


class GlobalDataClass(QObject):
    """Stores the global data available everywhere in the app."""

    filename_changed = pyqtSignal('QString')

    # A character has been added to the end
    character_added = pyqtSignal()

    # The character at index has been removed
    character_removed = pyqtSignal(int)

    # The characters have changed completely.
    characters_reset = pyqtSignal()

    race_added = pyqtSignal()
    race_removed = pyqtSignal(int)
    races_reset = pyqtSignal()

    def __init__(self):
        super(GlobalDataClass, self).__init__()
        self.filename = None
        self.universe = Universe.new()
        self.races = self.universe.races
        self.characters = self.universe.characters

    def open(self, filename):
        self.universe.load_from_json(filename)
        self.characters_reset.emit()
        self.races_reset.emit()

        if filename != self.filename:
            self.filename = filename
            self.filename_changed.emit(self.filename)

    def save(self, filename=None):
        filename = filename or self.filename
        self.universe.save_to_json(filename)
        if filename != self.filename:
            self.filename = filename
            self.filename_changed.emit(self.filename)

    def new(self):
        self.filename = None
        self.universe = Universe.new()
        self.characters_reset.emit()
        self.races_reset.emit()

    def createCharacter(self, **data):
        character = Character(self.universe, **data)
        self.universe.characters.append(character)
        self.character_added.emit()
        return character

    def createRace(self, **data):
        race = Race(self.universe, **data)
        self.universe.races.append(race)
        self.race_added.emit()
        return race

GlobalData = GlobalDataClass()
