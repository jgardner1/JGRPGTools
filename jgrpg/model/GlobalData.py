from .Race import Race
from .Character import Character
from .Item import Item
from .Skill import Skill
from .Personality import Personality

from PyQt5.QtCore import QObject, pyqtSignal

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
        self.characters = []
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
            backgrounds=[]
    ):
        self.characters[:] = [Character(**data) for data in characters]
        self.races[:] = [Race(**data) for data in races]
        self.skills[:] = [Skill(**data) for data in skills]
        self.personalities[:] = [Personality(**data)
            for data in personalities]
        self.backgrounds[:] = [Background(**data) for data in backgrounds]

        self.characters_reset.emit()
        self.races_reset.emit()
        self.skills_reset.emit()
        self.personalities_reset.emit()


    def save(self, filename=None):
        filename = filename or self.filename
        self.save_to_json(filename)
        if filename != self.filename:
            self.filename = filename
            self.filename_changed.emit(self.filename)

    def save_to_json(self, f):
        data = json.dump({
            'characters':[_.json() for _ in self.characters],
            'races':[_.json() for _ in self.races],
            'skills':[_.json() for _ in self.skills],
            'personalities':[_.json() for _ in self.personalities],
        }, open(f, 'w', encoding='utf8'), indent=2)

    def createCharacter(self, **data):
        character = Character(**data)
        self.characters.append(character)
        self.character_added.emit()
        return character

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
