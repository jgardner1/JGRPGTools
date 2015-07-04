import json

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from random import choice, uniform
from .Race import Race

from .Character import Characters
from .Item import ItemPrototypes
from .Group import Groups
from .ObjectStore import ObjectStore


class Skill(QObject):
    """A skill is something creatures can learn."""
    changed = pyqtSignal()

    def __init__(self, *, name=""):
        super(Skill, self).__init__()
        self.name = name

    def json(self):
        return {
            'name':self.name,
        }

class Personality(QObject):
    """A personality trait is something that the creature cannot learn and
    cannot easily change."""
    changed = pyqtSignal()

    def __init__(self, *, name=""):
        super(Personality, self).__init__()
        self.name = name

    def json(self):
        return {
            'name':self.name,
        }

class Background(QObject):
    changed = pyqtSignal()
    def __init__(self, *, name=""):
        super(Background, self).__init__()
        self.name = name

    def json(self):
        return {
            'name':self.name,
        }

class GlobalDataClass(QObject):
    """Stores the global data available everywhere in the app."""

    filename_changed = pyqtSignal('QString')

    race_added = pyqtSignal()
    race_removed = pyqtSignal(int)
    races_reset = pyqtSignal()

    skill_added = pyqtSignal()
    skill_removed = pyqtSignal(int)
    skills_reset = pyqtSignal()

    personality_added = pyqtSignal()
    personality_removed = pyqtSignal(int)
    personalities_reset = pyqtSignal()

    background_added = pyqtSignal()
    background_removed = pyqtSignal(int)
    backgrounds_reset = pyqtSignal()

    def __init__(self):
        super(GlobalDataClass, self).__init__()
        self.filename = None

        # Never reassign these. If you'd like to replace the array, use
        # self.races[:] = [...]
        self.races = []
        self.skills = []
        self.personalities = []
        self.backgrounds = []

        self.new()

    def new(self):
        self.load_from_json('default.jgu')
        
        self.filename = None

    def open(self, filename):
        self.load_from_json(filename)

        if filename != self.filename:
            self.filename = filename
            self.filename_changed.emit(self.filename)

    def load_from_json(self, f):
        data = json.load(open(f, 'r', encoding='utf8'))
        self.init_from_data(**data)

    def init_from_data(self, *,
            characters=[],
            races=[],
            skills=[],
            personalities=[],
            backgrounds=[],
            item_prototypes=[],
            groups=[]
    ):
        self.races[:] = [Race(**data) for data in races]
        self.skills[:] = [Skill(**data) for data in skills]
        self.personalities[:] = [Personality(**data)
            for data in personalities]
        self.backgrounds[:] = [Background(**data) for data in backgrounds]

        self.races_reset.emit()
        self.skills_reset.emit()
        self.personalities_reset.emit()

        Characters.load(characters)
        ItemPrototypes.load(item_prototypes)
        Groups.load(groups)


    def save(self, filename=None):
        filename = filename or self.filename
        self.save_to_json(filename)
        if filename != self.filename:
            self.filename = filename
            self.filename_changed.emit(self.filename)

    def save_to_json(self, f):
        data = json.dump({
            'characters':Characters.save(),
            'races':[_.json() for _ in self.races],
            'skills':[_.json() for _ in self.skills],
            'personalities':[_.json() for _ in self.personalities],
            'item_prototypes':ItemPrototypes.save(),
            'groups':Groups.save(),
        }, open(f, 'w', encoding='utf8'), indent=2)

    def createRace(self, **data):
        race = Race(**data)
        self.races.append(race)
        self.race_added.emit()
        return race 
    
    def deleteRace(self, race):
        index = self.races.index(race)
        self.races.pop(index)
        self.race_removed.emit(index)
        race.removed.emit()
        
    def createSkill(self, **data):
        skill = Skill(**data)
        self.skills.append(skill)
        self.skill_added.emit()
        return skill

    def createPersonality(self, **data):
        personality = Personality(**data)
        self.personalities.append(personality)
        self.personality_added.emit()
        return personality

    def createBackground(self, **data):
        background = Background(**data)
        self.backgrounds.append(background)
        self.background_added.emit()
        return background


GlobalData = GlobalDataClass()
